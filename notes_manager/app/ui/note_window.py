from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QCheckBox,
    QPushButton,
)


class NoteWindow(QWidget):
    def __init__(self, state, note_id):
        super().__init__()

        self.state = state
        self.note_id = note_id
        self.modified = False

        self.note = self.state.find_note(note_id)

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(self.note.text)

        self.pinned_box = QCheckBox("Pinned")
        self.pinned_box.setChecked(
            bool(self.note.pinned)
        )

        self.updated_label = QLabel(
            f"Updated: {self.note.created_at}"
        )

        self.close_button = QPushButton("Close")

        top = QHBoxLayout()
        top.addWidget(
            QLabel(f"Note {self.note_id}")
        )
        top.addStretch()
        top.addWidget(self.pinned_box)

        bottom = QHBoxLayout()
        bottom.addWidget(self.updated_label)
        bottom.addStretch()
        bottom.addWidget(self.close_button)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.text_edit)
        layout.addLayout(bottom)

        self.text_edit.textChanged.connect(
            self.text_changed
        )

        self.pinned_box.clicked.connect(
            self.pin_changed
        )

        self.close_button.clicked.connect(
            self.close
        )

        self.state.notes_changed.connect(
            self.reload_note
        )

        self.update_title()

    def update_title(self):
        star = "*" if self.modified else ""

        self.setWindowTitle(
            f"Note {self.note_id}{star} - Notes Manager"
        )

    def text_changed(self):
        self.modified = True
        self.update_title()

        text = self.text_edit.toPlainText()

        self.state.update_note(
            self.note_id,
            text
        )

        self.modified = False
        self.update_title()

    def pin_changed(self):
        note = self.state.find_note(self.note_id)

        if note:
            self.state.toggle_pin(
                self.note_id,
                note.pinned
            )

    def reload_note(self):
        note = self.state.find_note(self.note_id)

        if not note:
            self.close()
            return

        self.note = note

        self.updated_label.setText(
            f"Updated: {note.created_at}"
        )