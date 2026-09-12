from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QSpinBox,
    QDialogButtonBox,
)


class PreferencesDialog(QDialog):
    def __init__(self, state, parent=None):
        super().__init__(parent)

        self.state = state

        self.setWindowTitle("Preferences")

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel("Applies to every open window.")
        )

        self.pinned_first_box = QCheckBox(
            "Show pinned notes first"
        )
        self.pinned_first_box.setChecked(
            state.pinned_first
        )

        layout.addWidget(self.pinned_first_box)

        layout.addWidget(QLabel("Preview length:"))

        self.preview_spin = QSpinBox()
        self.preview_spin.setRange(10, 100)
        self.preview_spin.setValue(
            state.preview_length
        )

        layout.addWidget(self.preview_spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def accept(self):
        self.state.set_preferences(
            self.pinned_first_box.isChecked(),
            self.preview_spin.value()
        )

        super().accept()