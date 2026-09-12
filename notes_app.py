import sys
import sqlite3
from datetime import datetime

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QListWidget,
    QDockWidget,
    QToolBar,
    QLabel,
    QMessageBox,
)

STUDENT_NAME = "Yulian Mykhalchuk"
STUDENT_GROUP = "IT-32"
DB_FILE = "workspace_mykhalchuk.db"
SETTINGS_APP = "NotesAppYulianMykhalchuk"


class NotesWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"Notes - {STUDENT_NAME}, {STUDENT_GROUP}")
        self.resize(800, 500)

        self.connection = sqlite3.connect(DB_FILE)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

        self.settings = QSettings("Programming3Sem", SETTINGS_APP)

        self.note_editor = QTextEdit()
        self.setCentralWidget(self.note_editor)

        self.notes_list = QListWidget()

        self.notes_dock = QDockWidget("Notes", self)
        self.notes_dock.setWidget(self.notes_list)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.notes_dock)

        self.counter_label = QLabel("Notes: 0")

        self.statusBar().showMessage("Ready")
        self.statusBar().addPermanentWidget(self.counter_label)

        self.create_actions()
        self.create_menu()
        self.create_toolbar()

        self.notes_list.currentRowChanged.connect(self.load_note)

        self.load_notes()
        self.restore_window_state()

    def create_actions(self):
        self.new_action = QAction("New", self)
        self.save_action = QAction("Save", self)
        self.delete_action = QAction("Delete", self)
        self.exit_action = QAction("Exit", self)

        self.new_action.triggered.connect(self.new_note)
        self.save_action.triggered.connect(self.save_note)
        self.delete_action.triggered.connect(self.delete_note)
        self.exit_action.triggered.connect(self.close)

    def create_menu(self):
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.delete_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        view_menu = self.menuBar().addMenu("View")
        view_menu.addAction(self.notes_dock.toggleViewAction())

        help_menu = self.menuBar().addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        self.main_toolbar = QToolBar("Main")
        self.addToolBar(self.main_toolbar)

        self.main_toolbar.addAction(self.new_action)
        self.main_toolbar.addAction(self.save_action)
        self.main_toolbar.addAction(self.delete_action)

    def load_notes(self):
        self.notes_list.clear()

        self.cursor.execute(
            "SELECT id, text, created_at FROM notes ORDER BY id"
        )

        self.notes = self.cursor.fetchall()

        for note_id, text, created_at in self.notes:
            preview = text[:30]
            self.notes_list.addItem(
                f"{note_id}. {preview} ({created_at})"
            )

        self.counter_label.setText(f"Notes: {len(self.notes)}")

    def load_note(self, row):
        if row < 0 or row >= len(self.notes):
            return

        note_id, text, created_at = self.notes[row]
        self.note_editor.setPlainText(text)

    def new_note(self):
        self.notes_list.clearSelection()
        self.note_editor.clear()
        self.statusBar().showMessage("New note")

    def save_note(self):
        text = self.note_editor.toPlainText().strip()

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
                (text, note_id),
            )
        else:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

            self.cursor.execute(
                "INSERT INTO notes (text, created_at) VALUES (?, ?)",
                (text, created_at),
            )

        self.connection.commit()
        self.load_notes()

        self.note_editor.clear()
        self.statusBar().showMessage("Saved")

    def delete_note(self):
        row = self.notes_list.currentRow()

        if row < 0 or row >= len(self.notes):
            return

        note_id = self.notes[row][0]

        self.cursor.execute(
            "DELETE FROM notes WHERE id = ?",
            (note_id,),
        )

        self.connection.commit()

        self.note_editor.clear()
        self.load_notes()

        self.statusBar().showMessage("Deleted")

    def show_about(self):
        QMessageBox.information(
            self,
            "About",
            f"Notes App\n{STUDENT_NAME}, {STUDENT_GROUP}"
        )

    def restore_window_state(self):
        geometry = self.settings.value("geometry")
        state = self.settings.value("windowState")

        if geometry:
            self.restoreGeometry(geometry)

        if state:
            self.restoreState(state)

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        self.connection.close()

        event.accept()


app = QApplication(sys.argv)

window = NotesWindow()
window.show()

sys.exit(app.exec())