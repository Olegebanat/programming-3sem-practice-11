from PySide6.QtWidgets import QTextEdit


class NoteEditorPanel(QTextEdit):
    def get_text(self):
        return self.toPlainText().strip()