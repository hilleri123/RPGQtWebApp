from PyQt5.QtWidgets import QApplication, QDateTimeEdit, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QDateTime, Qt, pyqtSignal


class DateTimeEditWidget(QWidget):
    # Сигнал для кнопки "sync"
    need_to_sync = pyqtSignal()
    dateTimeChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Основной виджет QDateTimeEdit
        self.date_time_edit = QDateTimeEdit()
        self.date_time_edit.setReadOnly(True)  # Устанавливаем режим только для чтения
        self.date_time_edit.dateTimeChanged.connect(self.dateTimeChanged)
        self.date_time_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.date_time_edit.setMinimumSize(150, 30)  # Минимальный размер для QDateTimeEdit

        # Кнопки управления
        self.add_hour_button = QPushButton("+h")
        self.subtract_hour_button = QPushButton("-h")
        self.add_day_button = QPushButton("+d")
        self.subtract_day_button = QPushButton("-d")

        # Устанавливаем минимальные размеры кнопок
        button_size = (40, 30)  # Ширина и высота кнопок
        for button in [self.add_hour_button, self.subtract_hour_button, self.add_day_button, self.subtract_day_button]:
            button.setMinimumSize(*button_size)
            button.setMaximumSize(*button_size)

        # Подключаем кнопки к методам
        self.add_hour_button.clicked.connect(self.add_hour)
        self.subtract_hour_button.clicked.connect(self.subtract_hour)
        self.add_day_button.clicked.connect(self.add_day)
        self.subtract_day_button.clicked.connect(self.subtract_day)

        # Расположение кнопок и виджета
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)  # Уменьшаем отступы макета
        layout.setSpacing(5)  # Уменьшаем расстояние между элементами

        layout.addWidget(self.date_time_edit)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(2)  # Уменьшаем расстояние между кнопками
        button_layout.addWidget(self.add_day_button)
        button_layout.addWidget(self.add_hour_button)
        button_layout.addWidget(self.subtract_hour_button)
        button_layout.addWidget(self.subtract_day_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def add_hour(self):
        current_datetime = self.date_time_edit.dateTime()
        new_datetime = current_datetime.addSecs(3600)  # 3600 секунд = 1 час
        self.date_time_edit.setDateTime(new_datetime)

    def subtract_hour(self):
        current_datetime = self.date_time_edit.dateTime()
        new_datetime = current_datetime.addSecs(-3600)  # -3600 секунд = -1 час
        self.date_time_edit.setDateTime(new_datetime)

    def add_day(self):
        current_datetime = self.date_time_edit.dateTime()
        new_datetime = current_datetime.addDays(1)  # Добавляем 1 день
        self.date_time_edit.setDateTime(new_datetime)

    def subtract_day(self):
        current_datetime = self.date_time_edit.dateTime()
        new_datetime = current_datetime.addDays(-1)  # Отнимаем 1 день
        self.date_time_edit.setDateTime(new_datetime)

    def emit_sync_signal(self):
        self.need_to_sync.emit()

    def dateTime(self):
        return self.date_time_edit.dateTime()

    def setDateTime(self, dt):
        if dt is not None:
            return self.date_time_edit.setDateTime(dt)

