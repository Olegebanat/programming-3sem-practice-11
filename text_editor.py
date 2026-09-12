import sys
import os

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QLabel,
)


STUDENT_NAME = "Yulian Mykhalchuk"
STUDENT_GROUP = "IT-32"


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_file = None
        self.modified = False

        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        self.resize(800, 500)

        self.char_label = QLabel("Chars: 0")
        self.statusBar().showMessage("Ready")
        self.statusBar().addPermanentWidget(self.char_label)

        self.create_actions()
        self.create_menu()

        self.editor.textChanged.connect(self.text_changed)

        self.update_title()

    def create_actions(self):
        self.new_action = QAction("New", self)
        self.new_action.setShortcut(QKeySequence("Ctrl+N"))
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction("Open...", self)
        self.open_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction("Save", self)
        self.save_action.setShortcut(QKeySequence("Ctrl+S"))
        self.save_action.triggered.connect(self.save_file)

        self.save_as_action = QAction("Save As...", self)
        self.save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self.save_as_action.triggered.connect(self.save_as)

        self.quit_action = QAction("Quit", self)
        self.quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        self.quit_action.triggered.connect(self.close)

        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about)

    def create_menu(self):
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.about_action)

    def text_changed(self):
        self.modified = True

        text = self.editor.toPlainText()
        self.char_label.setText(f"Chars: {len(text)}")

        self.update_title()

    def update_title(self):
        if self.current_file:
            name = os.path.basename(self.current_file)
        else:
            name = "Untitled"

        if self.modified:
            name += "*"

        self.setWindowTitle(
            f"{name} - Text Editor - {STUDENT_NAME}, {STUDENT_GROUP}"
        )

    def confirm_changes(self):
        if not self.modified:
            return True

        answer = QMessageBox.question(
            self,
            "Unsaved changes",
            "Save changes before continuing?",
            QMessageBox.Save |
            QMessageBox.Discard |
            QMessageBox.Cancel,
        )

        if answer == QMessageBox.Save:
            return self.save_file()

        if answer == QMessageBox.Cancel:
            return False

        return True

    def new_file(self):
        if not self.confirm_changes():
            return

        self.editor.blockSignals(True)
        self.editor.clear()
        self.editor.blockSignals(False)

        self.current_file = None
        self.modified = False
        self.char_label.setText("Chars: 0")
        self.statusBar().showMessage("New file")

        self.update_title()

    def open_file(self):
        if not self.confirm_changes():
            return

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "Text Files (*.txt);;All Files (*)",
        )

        if not file_name:
            return

        try:
            with open(file_name, "r", encoding="utf-8") as file:
                text = file.read()

            self.editor.blockSignals(True)
            self.editor.setPlainText(text)
            self.editor.blockSignals(False)

            self.current_file = file_name
            self.modified = False
            self.char_label.setText(f"Chars: {len(text)}")
            self.statusBar().showMessage("File opened")

            self.update_title()

        except OSError:
            QMessageBox.critical(
                self,
                "Error",
                "Could not open file."
            )

    def save_file(self):
        if not self.current_file:
            return self.save_as()

        try:
            with open(
                self.current_file,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(self.editor.toPlainText())

            self.modified = False
            self.statusBar().showMessage("File saved")

            self.update_title()
            return True

        except OSError:
            QMessageBox.critical(
                self,
                "Error",
                "Could not save file."
            )
            return False

    def save_as(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save As",
            "",
            "Text Files (*.txt)",
        )

        if not file_name:
            return False

        if not file_name.endswith(".txt"):
            file_name += ".txt"

        self.current_file = file_name

        return self.save_file()

    def show_about(self):
        QMessageBox.about(
            self,
            "About",
            f"Text Editor\n{STUDENT_NAME}, {STUDENT_GROUP}"
        )

    def closeEvent(self, event):
        if self.confirm_changes():
            event.accept()
        else:
            event.ignore()


app = QApplication(sys.argv)

window = TextEditor()
window.show()

sys.exit(app.exec())