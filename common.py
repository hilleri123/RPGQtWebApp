import os
import shutil
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QLabel, QWidget, QListWidget
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent
from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QSize, Qt
import typing
# from PyQt5.QtGui import Qt

class AutoResizingTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.previous_width = 0

        self.textChanged.connect(self.auto_resize)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        current_width = self.width()
        if current_width != self.previous_width:
            self.previous_width = current_width
            self.auto_resize()

    def auto_resize(self):
        document = self.document()
        margins = self.contentsMargins()
        document.setTextWidth(self.viewport().width())
        height = margins.top() + document.size().height() + margins.bottom()
        size = QSize(self.width(), int(height))
        # self.setMaximumSize(size)
        self.setMaximumHeight(int(height+1))
    
class AutoResizingListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.previous_width = 0

        self.itemChanged.connect(self.auto_resize)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        current_width = self.width()
        if current_width != self.previous_width:
            self.previous_width = current_width
            self.auto_resize()

    def auto_resize(self):
        margins = self.contentsMargins()
        frame_width = self.frameWidth()
        total_height = 0
        for index in range(self.count()):
            item = self.item(index)
            total_height += self.visualItemRect(item).height()
        total_height += margins.top() + margins.bottom() + frame_width * 2
        # width = self.sizeHintForColumn(0) + margins.left() + margins.right() + frame_width * 2
        # size = QSize(width, total_height)
        # self.setMaximumSize(size)
        self.setMaximumHeight(int(total_height+1))


class BaseMapLabel(QLabel):
    item_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.original = QPixmap()
        self.map = None
        self.session = None
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
        if item is None or self.original.width() == 0 or self.original.height():
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
            if os.path.isfile(os.path.join((destination_directory, file_name))):
                print(f"Warning: Файл с именем '{file_name}' уже существует в директории '{destination_directory}'.")

            destination_path = os.path.join(destination_directory, file_name)
            shutil.copy2(file_path, destination_path)

            self.map.filePath = file_name
            self.session.commit()
            self.set_map()

    def add_item(self):
        pass


class BaseMapWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumSize(700, 500)
        base_layout = QVBoxLayout()
        self.setLayout(base_layout)
        self.mapLabel = None
        self.setup_label()
        base_layout.addWidget(self.mapLabel)
        self.button_layout = QHBoxLayout()
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