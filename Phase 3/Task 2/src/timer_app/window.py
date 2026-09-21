from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
)

from PySide6.QtCore import Qt

from .buttons import Buttons
from .stack import TimerStack


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Countdown Timer"
        )

        self.setMinimumSize(
            420,
            300
        )

        # -------------------------
        # Main widget/layout
        # -------------------------

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        layout = QVBoxLayout(
            central_widget
        )

        layout.setContentsMargins(
            30,
            30,
            30,
            30
        )

        layout.setSpacing(20)

        # -------------------------
        # Title
        # -------------------------

        title = QLabel(
            "Countdown Timer"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 26px;
                font-weight: bold;
            }
            """
        )

        # -------------------------
        # Components
        # -------------------------

        self.stack = TimerStack()

        self.buttons = Buttons()

        layout.addWidget(
            title
        )

        layout.addWidget(
            self.stack
        )

        layout.addWidget(
            self.buttons
        )

        # -------------------------
        # Connections
        # -------------------------

        self.buttons.start_clicked.connect(
            self._handle_start_button
        )

        self.buttons.reset_clicked.connect(
            self._reset
        )

        self.stack.timer_started.connect(
            self._timer_started
        )

        self.stack.timer_paused.connect(
            self._timer_paused
        )

        self.stack.timer_resumed.connect(
            self._timer_resumed
        )

        self.stack.timer_finished.connect(
            self._timer_finished
        )

        self._apply_style()

    def _handle_start_button(self):

        self.stack.start_or_pause()

    def _timer_started(self):

        self.buttons.show_pause()

    def _timer_paused(self):

        self.buttons.show_start()

    def _timer_resumed(self):

        self.buttons.show_pause()

    def _timer_finished(self):

        self._reset()

    def _reset(self):

        self.stack.reset()

        self.buttons.show_start()

    def _apply_style(self):

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f4f4f4;
            }

            QLineEdit {
                font-size: 20px;
                padding: 10px;
                border: 2px solid #cccccc;
                border-radius: 8px;
                background-color: white;
                color: #111111;
            }

            QLabel {
                color: #222222;
            }

            QPushButton {
                font-size: 17px;
                padding: 10px;
                border-radius: 8px;
                background-color: #333333;
                color: white;
            }

            QPushButton:hover {
                background-color: #555555;
            }
            """
        )