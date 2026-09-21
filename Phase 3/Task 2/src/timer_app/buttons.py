from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
)


class Buttons(QWidget):
    start_clicked = Signal()
    reset_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.start_button = QPushButton("Start")
        self.reset_button = QPushButton("Reset")

        self.start_button.setMinimumHeight(42)
        self.reset_button.setMinimumHeight(42)

        layout = QHBoxLayout(self)

        layout.addWidget(self.start_button)
        layout.addWidget(self.reset_button)

        self.start_button.clicked.connect(
            self.start_clicked.emit
        )

        self.reset_button.clicked.connect(
            self.reset_clicked.emit
        )

    def show_pause(self):
        self.start_button.setText("Pause")

    def show_start(self):
        self.start_button.setText("Start")