from PySide6.QtWidgets import QListWidget


class NoteListPanel(QListWidget):
    def show_notes(self, notes):
        self.clear()

        for note in notes:
            marker = "[PIN] " if note.pinned else ""

            self.addItem(
                f"{marker}{note.id}. {note.text[:30]}"
            )