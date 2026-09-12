import sys
import time

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)

STUDENT_NAME = "Yulian Mykhalchuk"
STUDENT_GROUP = "IT-32"
APP_TITLE = "Task Demo"
STEP_COUNT = 10
SLEEP_MS = 500


class TaskWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.click_count = 0

        self.setWindowTitle(
            f"{APP_TITLE} - {STUDENT_NAME}, {STUDENT_GROUP}"
        )
        self.setFixedSize(400, 220)

        self.status_label = QLabel("Ready")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, STEP_COUNT)
        self.progress_bar.setValue(0)

        self.start_button = QPushButton("Start")
        self.click_button = QPushButton("Click me (0)")

        layout = QVBoxLayout(self)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)
        layout.addWidget(self.click_button)

        self.start_button.clicked.connect(self.start_task)
        self.click_button.clicked.connect(self.count_click)

    def start_task(self):
        self.status_label.setText("Working...")
        self.start_button.setEnabled(False)
        self.progress_bar.setValue(0)

        for step in range(1, STEP_COUNT + 1):
            time.sleep(SLEEP_MS / 1000)
            self.progress_bar.setValue(step)

        self.status_label.setText("Done")
        self.start_button.setEnabled(True)

    def count_click(self):
        self.click_count += 1
        self.click_button.setText(
            f"Click me ({self.click_count})"
        )


app = QApplication(sys.argv)

window = TaskWindow()
window.show()

sys.exit(app.exec())