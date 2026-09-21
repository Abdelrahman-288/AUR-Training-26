# Task 2 - PySide6 Countdown Timer

## Description

A simple countdown timer application built using PySide6.

The application allows the user to enter a time in seconds, start the countdown, pause/resume it, and reset the timer.

## Features

- Enter countdown time in seconds
- Input validation using `QIntValidator`
- Countdown displayed in `MM:SS` format
- Start / Pause / Resume functionality
- Reset button
- Automatic reset when the timer reaches `00:00`
- Uses `QStackedWidget` to switch between input and timer views
- Uses `QTimer` for countdown updates
- Modular project structure using PySide6 signals and slots

## Project Structure

```text
Task 2/
├── src/
│   └── timer_app/
│       ├── __init__.py
│       ├── __main__.py
│       ├── buttons.py
│       ├── stack.py
│       └── window.py
├── requirements.txt
├── README.md
└── .gitignore