from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QToolBar,
    QMessageBox,
)

from app.config import STUDENT_NAME, STUDENT_GROUP, APP_TITLE
from app.state import AppState
from app.ui.note_list_panel import NoteListPanel
from app.ui.note_editor_panel import NoteEditorPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.state = AppState()

        self.setWindowTitle(
            f"{APP_TITLE} - {STUDENT_NAME}, {STUDENT_GROUP}"
        )

        self.resize(850, 520)

        self.editor = NoteEditorPanel()
        self.setCentralWidget(self.editor)

        self.notes_list = NoteListPanel()

        dock = QDockWidget("Notes", self)
        dock.setWidget(self.notes_list)

        self.addDockWidget(
            Qt.LeftDockWidgetArea,
            dock
        )

        self.create_actions()
        self.create_menu()
        self.create_toolbar()

        self.notes_list.currentRowChanged.connect(
            self.load_note
        )

        self.refresh()

    def create_actions(self):
        self.new_action = QAction("New note", self)
        self.save_action = QAction("Save note", self)
        self.delete_action = QAction("Delete note", self)
        self.pin_action = QAction("Pin", self)
        self.quit_action = QAction("Quit", self)

        self.new_action.triggered.connect(self.new_note)
        self.save_action.triggered.connect(self.save_note)
        self.delete_action.triggered.connect(self.delete_note)
        self.pin_action.triggered.connect(self.pin_note)
        self.quit_action.triggered.connect(self.close)

    def create_menu(self):
        menu = self.menuBar().addMenu("Note")

        menu.addAction(self.new_action)
        menu.addAction(self.save_action)
        menu.addAction(self.delete_action)
        menu.addAction(self.pin_action)
        menu.addSeparator()
        menu.addAction(self.quit_action)

    def create_toolbar(self):
        toolbar = QToolBar("Main")

        toolbar.addAction(self.new_action)
        toolbar.addAction(self.save_action)
        toolbar.addAction(self.delete_action)
        toolbar.addAction(self.pin_action)

        self.addToolBar(toolbar)

    def refresh(self):
        self.notes_list.show_notes(
            self.state.notes
        )

        self.statusBar().showMessage(
            f"Notes: {len(self.state.notes)}"
        )

    def new_note(self):
        self.notes_list.clearSelection()
        self.editor.clear()

    def save_note(self):
        text = self.editor.get_text()

        if not text:
            QMessageBox.warning(
                self,
                "Warning",
                "Note cannot be empty."
            )
            return

        self.state.add_note(text)

        self.editor.clear()

        self.refresh()

    def load_note(self, row):
        if row < 0 or row >= len(self.state.notes):
            return

        note = self.state.notes[row]

        self.editor.setPlainText(note.text)

    def delete_note(self):
        row = self.notes_list.currentRow()

        if row < 0:
            return

        note = self.state.notes[row]

        self.state.delete_note(note.id)

        self.editor.clear()

        self.refresh()

    def pin_note(self):
        row = self.notes_list.currentRow()

        if row < 0:
            return

        note = self.state.notes[row]

        self.state.toggle_pin(
            note.id,
            note.pinned
        )

        self.refresh()

    def closeEvent(self, event):
        self.state.storage.close()
        event.accept()