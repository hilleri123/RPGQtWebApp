import os
import shutil
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QLabel, QWidget, QListWidget
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent
from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QSize, Qt
import typing
from scheme import SceneMap, Session, IS_EDITABLE
# from PyQt5.QtGui import Qt



class BaseMapLabel(QLabel):
    item_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.original = QPixmap()
        self.map = None
        self.session = Session()
        self.items = []

    def mousePressEvent(self, ev: typing.Optional[QMouseEvent]) -> None:
        if ev is None:
            return
        pos = ev.pos()

        for item in self.items:
            if self.item_rect(item).contains(pos):
                self.item_clicked.emit(item.id)
                break

    def paintEvent(self, a0: typing.Optional[QPaintEvent]) -> None:
        super().paintEvent(a0)
        painter = QPainter(self)
        painter.setPen(QColor(255, 0, 0))

        for item in self.items:
            painter.drawRect(self.item_rect(item))

    def item_rect(self, item) -> QRect:
        if item is None or self.original.width() == 0 or self.original.height() == 0:
            return QRect()
        w_aspect = self.size().width() / self.original.width()
        h_aspect = self.size().height() / self.original.height()
        return QRect(QPoint(int(item.offsetX * w_aspect),
                     int(item.offsetY * h_aspect)),
                     QSize(int(item.width * w_aspect),
                     int(item.height * h_aspect)))

    def set_file_path(self, file_path):
        if self.map is not None and self.session is not None:
            file_name = os.path.basename(file_path)
            destination_directory = 'data/imgs'
            if os.path.isfile(os.path.join(destination_directory, file_name)):
                print(f"Warning: Файл с именем '{file_name}' уже существует в директории '{destination_directory}'.")

            destination_path = os.path.join(destination_directory, file_name)
            shutil.copy2(file_path, destination_path)

            self.map.filePath = file_name
            self.session.commit()
            self.set_map()

    def add_item(self):
        pass


class BaseMapWidget(QWidget):
    map_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumSize(700, 500)
        self.session = Session()
        base_layout = QVBoxLayout()
        self.setLayout(base_layout)
        self.mapLabel = None
        self.setup_label()
        base_layout.addWidget(self.mapLabel)
        self.button_layout = QHBoxLayout()
        if IS_EDITABLE:
            base_layout.addLayout(self.button_layout)
        self.select_file_button = QPushButton("select file")
        self.select_file_button.clicked.connect(self.open_file_dialog)
        self.button_layout.addWidget(self.select_file_button)
        self.add_item_button = QPushButton("add item")
        self.add_item_button.clicked.connect(self.add_item)
        self.button_layout.addWidget(self.add_item_button)

    def setup_label(self):
        self.mapLabel = BaseMapLabel()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        # Открываем диалог выбора файла
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp);;Все файлы (*)",
            options=options
        )
        if file_name:
            self.mapLabel.set_file_path(file_name)

    def add_item(self):
        self.mapLabel.add_item()

    def set_current_map(self, map_id: int):
        record_to_update = self.session.query(SceneMap) \
            .filter(SceneMap.isCurrent == True).first()
        if record_to_update is not None:
            record_to_update.isCurrent = False
        # print(record_to_update.name, record_to_update.isCurrent)
        record_to_update = self.session.query(SceneMap) \
            .filter(SceneMap.id == map_id).first()
        if record_to_update is not None:
            record_to_update.isCurrent = True
        # print(record_to_update.name, record_to_update.isCurrent)
        self.session.commit()
        self.mapLabel.set_map()
        self.map_changed.emit(map_id)