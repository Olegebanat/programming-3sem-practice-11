import sys
import sqlite3
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

STUDENT_NAME = "Yulian Mykhalchuk"
STUDENT_GROUP = "IT-32"
DB_FILE = "workspace_mykhalchuk.db"


class WorkspacePanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Workspace Panel")
        self.resize(700, 450)

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

        self.title_label = QLabel(
            f"{STUDENT_NAME}, {STUDENT_GROUP}"
        )

        self.counter_label = QLabel("Notes: 0")

        self.note_field = QLineEdit()
        self.note_field.setPlaceholderText("Enter note")

        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete last")
        self.clear_button = QPushButton("Clear all")

        self.preview_label = QLabel()
        self.preview_label.setWordWrap(True)

        self.status_label = QLabel(
            f"Database: {DB_FILE}"
        )

        self.quit_button = QPushButton("Quit")

        header = QHBoxLayout()
        header.addWidget(self.title_label)
        header.addStretch()
        header.addWidget(self.counter_label)

        input_row = QHBoxLayout()
        input_row.addWidget(self.add_button)
        input_row.addWidget(self.note_field)

        buttons_row = QHBoxLayout()
        buttons_row.addWidget(self.delete_button)
        buttons_row.addWidget(self.clear_button)

        footer = QHBoxLayout()
        footer.addWidget(self.status_label)
        footer.addStretch()
        footer.addWidget(self.quit_button)

        layout = QVBoxLayout()
        layout.addLayout(header)
        layout.addLayout(input_row)
        layout.addLayout(buttons_row)
        layout.addWidget(self.preview_label)
        layout.addStretch()
        layout.addLayout(footer)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_note)
        self.delete_button.clicked.connect(self.delete_last)
        self.clear_button.clicked.connect(self.clear_all)
        self.quit_button.clicked.connect(self.close)

        self.refresh()

    def refresh(self):
        self.cursor.execute(
            "SELECT created_at, text FROM notes ORDER BY id"
        )

        notes = self.cursor.fetchall()

        if notes:
            text = "\n".join(
                f"{created_at} {note}"
                for created_at, note in notes
            )
        else:
            text = "No notes yet"

        self.preview_label.setText(text)
        self.counter_label.setText(
            f"Notes: {len(notes)}"
        )

    def add_note(self):
        text = self.note_field.text().strip()

        if not text:
            return

        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        self.cursor.execute(
            "INSERT INTO notes (text, created_at) VALUES (?, ?)",
            (text, created_at),
        )

        self.connection.commit()
        self.note_field.clear()
        self.refresh()

    def delete_last(self):
        self.cursor.execute(
            """
            DELETE FROM notes
            WHERE id = (
                SELECT MAX(id) FROM notes
            )
            """
        )

        self.connection.commit()
        self.refresh()

    def clear_all(self):
        self.cursor.execute(
            "DELETE FROM notes"
        )

        self.connection.commit()
        self.refresh()

    def closeEvent(self, event):
        self.connection.close()
        super().closeEvent(event)


app = QApplication(sys.argv)

window = WorkspacePanel()
window.show()

sys.exit(app.exec())