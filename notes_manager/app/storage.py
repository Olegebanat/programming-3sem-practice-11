import sqlite3
from datetime import datetime

from app.config import DB_FILE
from app.models import Note


class StorageError(Exception):
    pass


class SqliteStorage:
    def __init__(self):
        try:
            self.connection = sqlite3.connect(DB_FILE)
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    pinned INTEGER NOT NULL DEFAULT 0
                )
                """
            )

            self.connection.commit()

        except sqlite3.Error as error:
            raise StorageError(str(error))

    def get_notes(self, pinned_first=True):
        order = "pinned DESC, id" if pinned_first else "id"

        self.cursor.execute(
            f"""
            SELECT id, text, created_at, pinned
            FROM notes
            ORDER BY {order}
            """
        )

        return [Note(*row) for row in self.cursor.fetchall()]

    def add_note(self, text):
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        self.cursor.execute(
            """
            INSERT INTO notes (text, created_at, pinned)
            VALUES (?, ?, 0)
            """,
            (text, created_at)
        )

        self.connection.commit()

    def update_note(self, note_id, text):
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        self.cursor.execute(
            """
            UPDATE notes
            SET text = ?, created_at = ?
            WHERE id = ?
            """,
            (text, created_at, note_id)
        )

        self.connection.commit()

    def delete_note(self, note_id):
        self.cursor.execute(
            "DELETE FROM notes WHERE id = ?",
            (note_id,)
        )
        self.connection.commit()

    def toggle_pin(self, note_id, pinned):
        self.cursor.execute(
            "UPDATE notes SET pinned = ? WHERE id = ?",
            (0 if pinned else 1, note_id)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()