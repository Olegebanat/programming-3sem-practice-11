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

from app.ui.note_editor_panel import NoteEditorPanel
from app.ui.note_table_model import NoteTableModel
from app.ui.note_table_view import NoteTableView
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
        self.resize(900, 520)

        self.editor = NoteEditorPanel()
        self.setCentralWidget(self.editor)

        self.table = NoteTableView()
        self.model = NoteTableModel(self.state)
        self.table.setModel(self.model)

        dock = QDockWidget("Notes", self)
        dock.setWidget(self.table)

        self.addDockWidget(
            Qt.LeftDockWidgetArea,
            dock
        )

        self.create_actions()
        self.create_menu()
        self.create_toolbar()

        self.table.clicked.connect(
            self.load_note
        )

        self.table.doubleClicked.connect(
            self.open_note_window
        )

        self.state.notes_changed.connect(
            self.refresh_status
        )

        self.refresh_status()

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
            self.open_selected_note
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

        toolbar.addAction(
            self.pin_action
        )

        toolbar.addSeparator()

        toolbar.addAction(
            self.open_window_action
        )

        self.addToolBar(toolbar)

    def selected_note(self):
        index = self.table.currentIndex()

        if not index.isValid():
            return None

        return self.model.note_at(
            index.row()
        )

    def load_note(self, index):
        note = self.model.note_at(
            index.row()
        )

        if note:
            self.editor.setPlainText(
                note.text
            )

    def new_note(self):
        self.table.clearSelection()
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

    def delete_note(self):
        note = self.selected_note()

        if note:
            self.state.delete_note(
                note.id
            )

            self.editor.clear()

    def pin_note(self):
        note = self.selected_note()

        if note:
            self.state.toggle_pin(
                note.id,
                note.pinned
            )

    def open_selected_note(self):
        note = self.selected_note()

        if note:
            self.manager.open_note_window(
                note.id
            )

    def open_note_window(self, index):
        note = self.model.note_at(
            index.row()
        )

        if note:
            self.manager.open_note_window(
                note.id
            )

    def open_preferences(self):
        dialog = PreferencesDialog(
            self.state,
            self
        )

        dialog.exec()

    def refresh_status(self):
        self.statusBar().showMessage(
            f"Window: {self.number} | "
            f"Notes: {len(self.state.notes)}"
        )