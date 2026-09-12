from app.storage import SqliteStorage


class AppState:
    def __init__(self):
        self.storage = SqliteStorage()
        self.notes = []

        self.refresh()

    def refresh(self):
        self.notes = self.storage.get_notes()

    def add_note(self, text):
        self.storage.add_note(text)
        self.refresh()

    def delete_note(self, note_id):
        self.storage.delete_note(note_id)
        self.refresh()

    def toggle_pin(self, note_id, pinned):
        self.storage.toggle_pin(note_id, pinned)
        self.refresh()