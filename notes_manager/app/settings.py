from PySide6.QtCore import QObject, QSettings, QByteArray

from app.config import ORG_NAME, APP_TITLE


class AppSettings(QObject):
    def __init__(self):
        super().__init__()

        self.settings = QSettings(
            ORG_NAME,
            APP_TITLE
        )

    def font_size(self):
        value = self.settings.value(
            "ui/font_size",
            12,
            int
        )

        return max(8, min(32, value))

    def set_font_size(self, value):
        self.settings.setValue(
            "ui/font_size",
            max(8, min(32, value))
        )

    def preview_length(self):
        value = self.settings.value(
            "ui/preview_length",
            40,
            int
        )

        return max(10, min(200, value))

    def set_preview_length(self, value):
        self.settings.setValue(
            "ui/preview_length",
            max(10, min(200, value))
        )

    def autosave(self):
        return self.settings.value(
            "editor/autosave",
            True,
            bool
        )

    def set_autosave(self, value):
        self.settings.setValue(
            "editor/autosave",
            value
        )

    def autosave_interval(self):
        value = self.settings.value(
            "editor/autosave_interval_s",
            30,
            int
        )

        return max(5, min(600, value))

    def set_autosave_interval(self, value):
        self.settings.setValue(
            "editor/autosave_interval_s",
            max(5, min(600, value))
        )

    def confirm_delete(self):
        return self.settings.value(
            "editor/confirm_delete",
            True,
            bool
        )

    def set_confirm_delete(self, value):
        self.settings.setValue(
            "editor/confirm_delete",
            value
        )

    def log_level(self):
        value = self.settings.value(
            "logging/level",
            "INFO",
            str
        )

        if value not in ("INFO", "DEBUG"):
            return "INFO"

        return value

    def set_log_level(self, value):
        if value not in ("INFO", "DEBUG"):
            value = "INFO"

        self.settings.setValue(
            "logging/level",
            value
        )

    def window_geometry(self):
        return self.settings.value(
            "window/geometry",
            QByteArray(),
            QByteArray
        )

    def set_window_geometry(self, value):
        self.settings.setValue(
            "window/geometry",
            value
        )

    def window_state(self):
        return self.settings.value(
            "window/state",
            QByteArray(),
            QByteArray
        )

    def set_window_state(self, value):
        self.settings.setValue(
            "window/state",
            value
        )