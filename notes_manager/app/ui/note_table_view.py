from PySide6.QtWidgets import QTableView
from PySide6.QtCore import Qt


class NoteTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSelectionBehavior(
            QTableView.SelectRows
        )

        self.setSelectionMode(
            QTableView.SingleSelection
        )

        self.setEditTriggers(
            QTableView.NoEditTriggers
        )

        self.verticalHeader().setVisible(False)

        self.setAlternatingRowColors(True)

        self.horizontalHeader().setStretchLastSection(True)