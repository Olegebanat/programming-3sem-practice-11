import sys

from PySide6.QtWidgets import QApplication

from app.state import AppState
from app.ui.window_manager import WindowManager


app = QApplication(sys.argv)

state = AppState()

manager = WindowManager(state)

manager.open_main_window()

result = app.exec()

state.storage.close()

sys.exit(result)