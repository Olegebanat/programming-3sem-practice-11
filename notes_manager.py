import sys
import csv
import sqlite3
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QListWidget,
    QDockWidget,
    QToolBar,
    QLabel,
    QMessageBox,
    QFileDialog,
    QToolButton,
    QMenu,
)

STUDENT_NAME = "Yulian Mykhalchuk"
STUDENT_GROUP = "IT-32"
DB_FILE = "workspace_mykhalchuk.db"


class NotesManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            f"Notes Manager - {STUDENT_NAME}, {STUDENT_GROUP}"
        )
        self.resize(850, 520)

        self.connection = sqlite3.connect(DB_FILE)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL,
                pinned INTEGER NOT NULL DEFAULT 0
            )
            """
        )

        try:
            self.cursor.execute(
                "ALTER TABLE notes ADD COLUMN pinned INTEGER NOT NULL DEFAULT 0"
            )
        except sqlite3.OperationalError:
            pass

        self.connection.commit()

        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        self.notes_list = QListWidget()
        self.notes_dock = QDockWidget("Notes", self)
        self.notes_dock.setWidget(self.notes_list)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.notes_dock)

        self.filter_label = QLabel("Filter: All")
        self.counter_label = QLabel("Notes: 0")

        self.statusBar().showMessage("Ready")
        self.statusBar().addPermanentWidget(self.filter_label)
        self.statusBar().addPermanentWidget(self.counter_label)

        self.current_filter = "all"

        self.create_actions()
        self.create_menu()
        self.create_toolbar()

        self.notes_list.currentRowChanged.connect(self.load_note)

        self.load_notes()

    def create_actions(self):
        self.new_action = QAction("New note", self)
        self.new_action.setShortcut(QKeySequence("Ctrl+N"))
        self.new_action.triggered.connect(self.new_note)

        self.save_action = QAction("Save note", self)
        self.save_action.setShortcut(QKeySequence("Ctrl+S"))
        self.save_action.triggered.connect(self.save_note)

        self.delete_action = QAction("Delete note", self)
        self.delete_action.setShortcut(QKeySequence("Delete"))
        self.delete_action.triggered.connect(self.delete_note)

        self.pin_action = QAction("Pin", self)
        self.pin_action.setShortcut(QKeySequence("Ctrl+P"))
        self.pin_action.triggered.connect(self.toggle_pin)

        self.clear_action = QAction("Clear all notes", self)
        self.clear_action.triggered.connect(self.clear_all)

        self.quit_action = QAction("Quit", self)
        self.quit_action.triggered.connect(self.close)

        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about)

        self.all_action = QAction("All", self)
        self.all_action.triggered.connect(
            lambda: self.set_filter("all")
        )

        self.pinned_action = QAction("Pinned", self)
        self.pinned_action.triggered.connect(
            lambda: self.set_filter("pinned")
        )

        self.other_action = QAction("Other", self)
        self.other_action.triggered.connect(
            lambda: self.set_filter("other")
        )

        self.export_txt_action = QAction("Export TXT", self)
        self.export_txt_action.triggered.connect(self.export_txt)

        self.export_csv_action = QAction("Export CSV", self)
        self.export_csv_action.triggered.connect(self.export_csv)

    def create_menu(self):
        note_menu = self.menuBar().addMenu("Note")
        note_menu.addAction(self.new_action)
        note_menu.addAction(self.save_action)
        note_menu.addAction(self.delete_action)
        note_menu.addAction(self.pin_action)
        note_menu.addSeparator()
        note_menu.addAction(self.quit_action)

        edit_menu = self.menuBar().addMenu("Edit")
        edit_menu.addAction(self.clear_action)

        view_menu = self.menuBar().addMenu("View")
        view_menu.addAction(self.all_action)
        view_menu.addAction(self.pinned_action)
        view_menu.addAction(self.other_action)

        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.about_action)

    def create_toolbar(self):
        toolbar = QToolBar("Main")
        self.addToolBar(toolbar)

        toolbar.addAction(self.new_action)
        toolbar.addAction(self.save_action)
        toolbar.addAction(self.delete_action)
        toolbar.addSeparator()

        toolbar.addAction(self.pin_action)
        toolbar.addSeparator()

        toolbar.addAction(self.all_action)
        toolbar.addAction(self.pinned_action)
        toolbar.addAction(self.other_action)
        toolbar.addSeparator()

        export_button = QToolButton()
        export_button.setText("Export")

        export_menu = QMenu(export_button)
        export_menu.addAction(self.export_txt_action)
        export_menu.addAction(self.export_csv_action)

        export_button.setMenu(export_menu)
        export_button.setPopupMode(QToolButton.InstantPopup)

        toolbar.addWidget(export_button)

    def load_notes(self):
        self.notes_list.clear()

        if self.current_filter == "pinned":
            self.cursor.execute(
                """
                SELECT id, text, created_at, pinned
                FROM notes
                WHERE pinned = 1
                ORDER BY id
                """
            )
        elif self.current_filter == "other":
            self.cursor.execute(
                """
                SELECT id, text, created_at, pinned
                FROM notes
                WHERE pinned = 0
                ORDER BY id
                """
            )
        else:
            self.cursor.execute(
                """
                SELECT id, text, created_at, pinned
                FROM notes
                ORDER BY pinned DESC, id
                """
            )

        self.notes = self.cursor.fetchall()

        for note_id, text, created_at, pinned in self.notes:
            marker = "[PIN] " if pinned else ""
            self.notes_list.addItem(
                f"{marker}{note_id}. {text[:30]}"
            )

        self.counter_label.setText(
            f"Notes: {len(self.notes)}"
        )

    def load_note(self, row):
        if row < 0 or row >= len(self.notes):
            return

        note_id, text, created_at, pinned = self.notes[row]
        self.editor.setPlainText(text)

    def new_note(self):
        self.notes_list.clearSelection()
        self.editor.clear()
        self.statusBar().showMessage("New note")

    def save_note(self):
        text = self.editor.toPlainText().strip()

        if not text:
            QMessageBox.warning(
                self,
                "Warning",
                "Note cannot be empty."
            )
            return

        row = self.notes_list.currentRow()

        if row >= 0 and row < len(self.notes):
            note_id = self.notes[row][0]

            self.cursor.execute(
                "UPDATE notes SET text = ? WHERE id = ?",
                (text, note_id)
            )
        else:
            created_at = datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )

            self.cursor.execute(
                """
                INSERT INTO notes (text, created_at, pinned)
                VALUES (?, ?, 0)
                """,
                (text, created_at)
            )

        self.connection.commit()
        self.load_notes()
        self.statusBar().showMessage("Saved")

    def delete_note(self):
        row = self.notes_list.currentRow()

        if row < 0 or row >= len(self.notes):
            return

        answer = QMessageBox.question(
            self,
            "Confirm",
            "Delete selected note?"
        )

        if answer == QMessageBox.Yes:
            note_id = self.notes[row][0]

            self.cursor.execute(
                "DELETE FROM notes WHERE id = ?",
                (note_id,)
            )

            self.connection.commit()
            self.editor.clear()
            self.load_notes()

    def toggle_pin(self):
        row = self.notes_list.currentRow()

        if row < 0 or row >= len(self.notes):
            return

        note_id, text, created_at, pinned = self.notes[row]

        self.cursor.execute(
            "UPDATE notes SET pinned = ? WHERE id = ?",
            (0 if pinned else 1, note_id)
        )

        self.connection.commit()
        self.load_notes()

    def clear_all(self):
        answer = QMessageBox.question(
            self,
            "Confirm",
            "Delete all notes?"
        )

        if answer == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM notes")
            self.connection.commit()
            self.editor.clear()
            self.load_notes()

    def set_filter(self, filter_name):
        self.current_filter = filter_name
        self.filter_label.setText(
            f"Filter: {filter_name.capitalize()}"
        )
        self.load_notes()

    def export_txt(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export TXT",
            "notes.txt",
            "Text Files (*.txt)"
        )

        if not file_name:
            return

        self.cursor.execute(
            "SELECT text, created_at, pinned FROM notes"
        )

        rows = self.cursor.fetchall()

        with open(file_name, "w", encoding="utf-8") as file:
            for text, created_at, pinned in rows:
                file.write(
                    f"{created_at} | pinned={pinned}\n{text}\n\n"
                )

    def export_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export CSV",
            "notes.csv",
            "CSV Files (*.csv)"
        )

        if not file_name:
            return

        self.cursor.execute(
            "SELECT id, text, created_at, pinned FROM notes"
        )

        rows = self.cursor.fetchall()

        with open(
            file_name,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(
                ["id", "text", "created_at", "pinned"]
            )
            writer.writerows(rows)

    def show_about(self):
        QMessageBox.information(
            self,
            "About",
            f"Notes Manager\n{STUDENT_NAME}, {STUDENT_GROUP}"
        )

    def closeEvent(self, event):
        self.connection.close()
        event.accept()


app = QApplication(sys.argv)

window = NotesManager()
window.show()

sys.exit(app.exec())