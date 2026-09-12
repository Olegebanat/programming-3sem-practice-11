from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

from app.config import TABLE_PREVIEW_LENGTH, EMPTY_TABLE_TEXT


class NoteTableModel(QAbstractTableModel):
    HEADERS = ["ID", "Pinned", "Preview", "Updated"]

    def __init__(self, state):
        super().__init__()
        self.state = state

        self.state.notes_changed.connect(self.refresh)

    def rowCount(self, parent=QModelIndex()):
        return len(self.state.notes)

    def columnCount(self, parent=QModelIndex()):
        return 4

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if index.row() >= len(self.state.notes):
            return None

        note = self.state.notes[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return note.id

            if index.column() == 1:
                return "Yes" if note.pinned else "No"

            if index.column() == 2:
                text = note.text.replace("\n", " ")

                if len(text) > TABLE_PREVIEW_LENGTH:
                    return text[:TABLE_PREVIEW_LENGTH] + "..."

                return text

            if index.column() == 3:
                return note.created_at

        if role == Qt.TextAlignmentRole:
            if index.column() in (0, 1):
                return Qt.AlignCenter

        return None

    def headerData(
        self,
        section,
        orientation,
        role=Qt.DisplayRole
    ):
        if (
            orientation == Qt.Horizontal
            and role == Qt.DisplayRole
        ):
            return self.HEADERS[section]

        return super().headerData(
            section,
            orientation,
            role
        )

    def note_at(self, row):
        if 0 <= row < len(self.state.notes):
            return self.state.notes[row]

        return None

    def refresh(self):
        self.beginResetModel()
        self.endResetModel()