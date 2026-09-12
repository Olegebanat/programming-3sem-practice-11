from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QToolBar,
    QMessageBox,
    QApplication,
)

from PySide6.QtCore import Qt

from app.config import (
    STUDENT_NAME,
    STUDENT_GROUP,
    APP_TITLE,
)

from app.ui.note_list_panel import NoteListPanel
from app.ui.note_editor_panel import NoteEditorPanel
from app.ui.preferences_dialog import PreferencesDialog


class MainWindow(QMainWindow):
    def __init__(self, state, manager, number):
        super().__init__()

        self.state = state
        self.manager = manager
        self.number = number

        if number == 1:
            title = (
                f"{APP_TITLE} - "
                f"{STUDENT_NAME}, {STUDENT_GROUP}"
            )
        else:
            title = (
                f"{APP_TITLE} ({number}) - "
                f"{STUDENT_NAME}, {STUDENT_GROUP}"
            )

        self.setWindowTitle(title)
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

        self.notes_list.itemDoubleClicked.connect(
            self.open_note_window
        )

        self.state.notes_changed.connect(
            self.refresh
        )

        self.state.settings_changed.connect(
            self.refresh
        )

        self.refresh()

    def create_actions(self):
        self.new_note_action = QAction(
            "New note",
            self
        )

        self.save_action = QAction(
            "Save note",
            self
        )

        self.delete_action = QAction(
            "Delete note",
            self
        )

        self.pin_action = QAction(
            "Pin",
            self
        )

        self.open_window_action = QAction(
            "Open in new window",
            self
        )

        self.open_window_action.setShortcut(
            QKeySequence("Ctrl+Return")
        )

        self.new_window_action = QAction(
            "New window",
            self
        )

        self.new_window_action.setShortcut(
            QKeySequence("Ctrl+Shift+N")
        )

        self.close_window_action = QAction(
            "Close window",
            self
        )

        self.close_window_action.setShortcut(
            QKeySequence("Ctrl+W")
        )

        self.preferences_action = QAction(
            "Preferences...",
            self
        )

        self.preferences_action.setShortcut(
            QKeySequence("Ctrl+,")
        )

        self.quit_action = QAction(
            "Quit",
            self
        )

        self.quit_action.setShortcut(
            QKeySequence("Ctrl+Q")
        )

        self.new_note_action.triggered.connect(
            self.new_note
        )

        self.save_action.triggered.connect(
            self.save_note
        )

        self.delete_action.triggered.connect(
            self.delete_note
        )

        self.pin_action.triggered.connect(
            self.pin_note
        )

        self.open_window_action.triggered.connect(
            self.open_note_window
        )

        self.new_window_action.triggered.connect(
            self.manager.open_main_window
        )

        self.close_window_action.triggered.connect(
            self.close
        )

        self.preferences_action.triggered.connect(
            self.open_preferences
        )

        self.quit_action.triggered.connect(
            QApplication.closeAllWindows
        )

    def create_menu(self):
        note_menu = self.menuBar().addMenu("Note")

        note_menu.addAction(
            self.new_note_action
        )
        note_menu.addAction(
            self.save_action
        )
        note_menu.addAction(
            self.delete_action
        )
        note_menu.addAction(
            self.pin_action
        )
        note_menu.addAction(
            self.open_window_action
        )
        note_menu.addSeparator()
        note_menu.addAction(
            self.quit_action
        )

        edit_menu = self.menuBar().addMenu("Edit")

        edit_menu.addAction(
            self.preferences_action
        )

        window_menu = self.menuBar().addMenu(
            "Window"
        )

        window_menu.addAction(
            self.new_window_action
        )
        window_menu.addAction(
            self.close_window_action
        )

        self.menuBar().addMenu("Help")

    def create_toolbar(self):
        toolbar = QToolBar("Main")

        toolbar.addAction(
            self.new_note_action
        )
        toolbar.addAction(
            self.save_action
        )
        toolbar.addAction(
            self.delete_action
        )

        toolbar.addSeparator()

        toolbar.addAction(
            self.open_window_action
        )

        self.addToolBar(toolbar)

    def refresh(self):
        self.notes_list.show_notes(
            self.state.notes,
            self.state.preview_length
        )

        self.statusBar().showMessage(
            f"Window: {self.number} | "
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

    def load_note(self, row):
        if row < 0 or row >= len(self.state.notes):
            return

        note = self.state.notes[row]

        self.editor.setPlainText(
            note.text
        )

    def delete_note(self):
        row = self.notes_list.currentRow()

        if row < 0:
            return

        note = self.state.notes[row]

        self.state.delete_note(
            note.id
        )

        self.editor.clear()

    def pin_note(self):
        row = self.notes_list.currentRow()

        if row < 0:
            return

        note = self.state.notes[row]

        self.state.toggle_pin(
            note.id,
            note.pinned
        )

    def open_note_window(self):
        row = self.notes_list.currentRow()

        if row < 0:
            return

        note = self.state.notes[row]

        self.manager.open_note_window(
            note.id
        )

    def open_preferences(self):
        dialog = PreferencesDialog(
            self.state,
            self
        )

        dialog.exec()