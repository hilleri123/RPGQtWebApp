from PyQt5.QtWidgets import QApplication, QDateTimeEdit, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QDateTime, Qt


class DateTimeEditWidget(QDateTimeEdit):
    def __init__(self):
        super().__init__()