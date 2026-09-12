from PySide6.QtCore import QObject, Signal

from app.storage import (
    SqliteStorage,
    StorageError,
)


class AppState(QObject):
    notes_changed = Signal()
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()

        self.notes = []
        self.storage = None

        try:
            self.storage = SqliteStorage()
            self.refresh()

        except StorageError as error:
            self.error_occurred.emit(
                str(error)
            )

    def refresh(self):
        if not self.storage:
            return

        try:
            self.notes = self.storage.get_notes()
            self.notes_changed.emit()

        except StorageError as error:
            self.error_occurred.emit(
                str(error)
            )

    def add_note(self, text):
        if not self.storage:
            return

        try:
            self.storage.add_note(text)
            self.refresh()

        except StorageError as error:
            self.error_occurred.emit(
                str(error)
            )

    def update_note(self, note_id, text):
        if not self.storage:
            return

        try:
            self.storage.update_note(
                note_id,
                text
            )

            self.refresh()

        except StorageError as error:
            self.error_occurred.emit(
                str(error)
            )

    def delete_note(self, note_id):
        if not self.storage:
            return

        try:
            self.storage.delete_note(
                note_id
            )

            self.refresh()

        except StorageError as error:
            self.error_occurred.emit(
                str(error)
            )

    def toggle_pin(self, note_id, pinned):
        if not self.storage:
            return

        try:
            self.storage.toggle_pin(
                note_id,
                pinned
            )

            self.refresh()

        except StorageError as error:
            self.error_occurred.emit(
                str(error)
            )

    def find_note(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note

        return None