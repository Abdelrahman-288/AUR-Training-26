from PySide6.QtCore import QTimer, Signal, Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QStackedWidget,
    QLineEdit,
    QLabel,
)


class TimerStack(QStackedWidget):
    timer_started = Signal()
    timer_paused = Signal()
    timer_resumed = Signal()
    timer_finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.remaining_seconds = 0
        self.running = False
        self.paused = False

        # -------------------------
        # Input page
        # -------------------------

        self.input_field = QLineEdit()

        self.input_field.setPlaceholderText(
            "Enter time in seconds"
        )

        self.input_field.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # Only allow positive integers
        validator = QIntValidator(1, 359999, self)

        self.input_field.setValidator(
            validator
        )

        self.input_field.setMinimumHeight(60)

        # -------------------------
        # Timer label page
        # -------------------------

        self.timer_label = QLabel("00:00")

        self.timer_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.timer_label.setMinimumHeight(100)

        # Add both pages to QStackedWidget
        self.addWidget(
            self.input_field
        )

        self.addWidget(
            self.timer_label
        )

        # Initially show QLineEdit
        self.setCurrentWidget(
            self.input_field
        )

        # -------------------------
        # QTimer
        # -------------------------

        self.timer = QTimer(self)

        self.timer.setInterval(1000)

        self.timer.timeout.connect(
            self._decrement
        )

    def start_or_pause(self):
        """
        Handles:
        Start
        Pause
        Resume
        """

        # -------------------------
        # Start timer
        # -------------------------

        if not self.running:

            text = self.input_field.text().strip()

            if not text:
                self._show_invalid_input()
                return False

            seconds = int(text)

            if seconds <= 0:
                self._show_invalid_input()
                return False

            self.remaining_seconds = seconds

            self.running = True
            self.paused = False

            self.input_field.setStyleSheet("")

            self._update_label()

            # Switch from QLineEdit to QLabel
            self.setCurrentWidget(
                self.timer_label
            )

            self.timer.start()

            self.timer_started.emit()

            return True

        # -------------------------
        # Pause timer
        # -------------------------

        if self.running and not self.paused:

            self.timer.stop()

            self.paused = True

            self.timer_paused.emit()

            return True

        # -------------------------
        # Resume timer
        # -------------------------

        if self.running and self.paused:

            self.timer.start()

            self.paused = False

            self.timer_resumed.emit()

            return True

        return False

    def _decrement(self):

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1

        self._update_label()

        if self.remaining_seconds <= 0:

            self.timer.stop()

            # Show 00:00 briefly before reset
            self.timer_label.setText(
                "00:00"
            )

            self.timer_finished.emit()

    def _update_label(self):

        minutes = self.remaining_seconds // 60

        seconds = self.remaining_seconds % 60

        self.timer_label.setText(
            f"{minutes:02d}:{seconds:02d}"
        )

    def reset(self):

        self.timer.stop()

        self.remaining_seconds = 0

        self.running = False
        self.paused = False

        # Clear input as required
        self.input_field.clear()

        self.input_field.setStyleSheet("")

        self.timer_label.setText(
            "00:00"
        )

        # Return to input page
        self.setCurrentWidget(
            self.input_field
        )

        self.input_field.setFocus()

    def _show_invalid_input(self):

        self.input_field.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid red;
            }
            """
        )

        self.input_field.setPlaceholderText(
            "Enter a valid number of seconds"
        )