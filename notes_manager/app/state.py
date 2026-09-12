from PySide6.QtCore import QObject, Signal

from app.config import DEFAULT_PREVIEW_LENGTH
from app.storage import SqliteStorage


class AppState(QObject):
    notes_changed = Signal()
    settings_changed = Signal()

    def __init__(self):
        super().__init__()

        self.storage = SqliteStorage()

        self.pinned_first = True
        self.preview_length = DEFAULT_PREVIEW_LENGTH

        self.notes = []
        self.refresh()

    def refresh(self):
        self.notes = self.storage.get_notes(
            self.pinned_first
        )
        self.notes_changed.emit()

    def add_note(self, text):
        self.storage.add_note(text)
        self.refresh()

    def update_note(self, note_id, text):
        self.storage.update_note(note_id, text)
        self.refresh()

    def delete_note(self, note_id):
        self.storage.delete_note(note_id)
        self.refresh()

    def toggle_pin(self, note_id, pinned):
        self.storage.toggle_pin(note_id, pinned)
        self.refresh()

    def set_preferences(self, pinned_first, preview_length):
        self.pinned_first = pinned_first
        self.preview_length = preview_length

        self.settings_changed.emit()
        self.refresh()

    def find_note(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note

        return None