import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class BusinessCard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Business Card - Yulian Mykhalchuk")
        self.setFixedSize(320, 200)

        name_label = QLabel("Yulian Mykhalchuk")
        group_label = QLabel("IT-32")
        course_label = QLabel("Python Programming, Semester 3")

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(group_label)
        layout.addWidget(course_label)
        layout.addWidget(close_button)

        self.setLayout(layout)

app = QApplication(sys.argv)
window = BusinessCard()
window.show()
sys.exit(app.exec())