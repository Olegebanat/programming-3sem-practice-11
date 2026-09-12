from app.config import CASCADE_STEP
from app.ui.main_window import MainWindow
from app.ui.note_window import NoteWindow


class WindowManager:
    def __init__(self, state):
        self.state = state

        self.main_windows = []
        self.note_windows = {}

    def open_main_window(self):
        number = len(self.main_windows) + 1

        window = MainWindow(
            self.state,
            self,
            number
        )

        offset = (number - 1) * CASCADE_STEP

        window.move(
            100 + offset,
            100 + offset
        )

        self.main_windows.append(window)

        window.destroyed.connect(
            lambda: self.remove_main(window)
        )

        window.show()

    def remove_main(self, window):
        if window in self.main_windows:
            self.main_windows.remove(window)

    def open_note_window(self, note_id):
        if note_id in self.note_windows:
            self.note_windows[note_id].raise_()
            self.note_windows[note_id].activateWindow()
            return

        window = NoteWindow(
            self.state,
            note_id
        )

        self.note_windows[note_id] = window

        window.destroyed.connect(
            lambda: self.note_windows.pop(
                note_id,
                None
            )
        )

        window.show()