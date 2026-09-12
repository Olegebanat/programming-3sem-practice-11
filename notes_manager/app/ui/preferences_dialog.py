from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QCheckBox,
    QComboBox,
    QDialogButtonBox,
)


class PreferencesDialog(QDialog):
    def __init__(
        self,
        settings,
        parent=None
    ):
        super().__init__(parent)

        self.settings = settings

        self.setWindowTitle(
            "Preferences"
        )

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel("Font size:")
        )

        self.font_size = QSpinBox()
        self.font_size.setRange(8, 32)
        self.font_size.setValue(
            settings.font_size()
        )

        layout.addWidget(
            self.font_size
        )

        layout.addWidget(
            QLabel("Preview length:")
        )

        self.preview_length = QSpinBox()
        self.preview_length.setRange(
            10,
            200
        )

        self.preview_length.setValue(
            settings.preview_length()
        )

        layout.addWidget(
            self.preview_length
        )

        self.autosave = QCheckBox(
            "Autosave"
        )

        self.autosave.setChecked(
            settings.autosave()
        )

        layout.addWidget(
            self.autosave
        )

        layout.addWidget(
            QLabel("Autosave interval:")
        )

        self.autosave_interval = QSpinBox()
        self.autosave_interval.setRange(
            5,
            600
        )

        self.autosave_interval.setValue(
            settings.autosave_interval()
        )

        layout.addWidget(
            self.autosave_interval
        )

        self.confirm_delete = QCheckBox(
            "Confirm delete"
        )

        self.confirm_delete.setChecked(
            settings.confirm_delete()
        )

        layout.addWidget(
            self.confirm_delete
        )

        layout.addWidget(
            QLabel("Log level:")
        )

        self.log_level = QComboBox()
        self.log_level.addItems(
            [
                "INFO",
                "DEBUG"
            ]
        )

        self.log_level.setCurrentText(
            settings.log_level()
        )

        layout.addWidget(
            self.log_level
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(buttons)

    def accept(self):
        self.settings.set_font_size(
            self.font_size.value()
        )

        self.settings.set_preview_length(
            self.preview_length.value()
        )

        self.settings.set_autosave(
            self.autosave.isChecked()
        )

        self.settings.set_autosave_interval(
            self.autosave_interval.value()
        )

        self.settings.set_confirm_delete(
            self.confirm_delete.isChecked()
        )

        self.settings.set_log_level(
            self.log_level.currentText()
        )

        super().accept()