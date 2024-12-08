import os
import shutil
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QLineEdit, QDateTimeEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QLabel, QWidget, QListWidget
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QPolygonF
from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QPointF, QSize, Qt
import typing
from scheme import *
from .datetime_editor import DateTimeEditWidget


TRIANGLE_SIZE = 15


class BaseMapLabel(QLabel):
    map_image_saved = pyqtSignal()
    item_clicked = pyqtSignal(int)
    time_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.original = QPixmap()
        self.pix_map_for_save = QPixmap()
        self.map = None
        self.items = []

    def mousePressEvent(self, ev: typing.Optional[QMouseEvent]) -> None:
        if ev is None:
            return
        pos = ev.pos()

        for item in self.items:
            if self.item_rect(item).contains(pos):
                if ev.button() == Qt.RightButton:
                    self.show_context_menu(ev.globalPos(), item)
                else:
                    self.item_clicked.emit(item.id)
                break

    def paintEvent(self, a0: typing.Optional[QPaintEvent]) -> None:
        super().paintEvent(a0)
        if self.original.isNull():
            return
        self.pix_map_for_save = self.original.copy()
        pix_map_painter = QPainter(self.pix_map_for_save)
        painter = QPainter(self)
        self.paint(painter, paint_hidden=True, scale=True)
        self.paint(pix_map_painter, paint_hidden=False, scale=False)

        self.saveImage()

    def paint(self, painter: QPainter, paint_hidden = False, scale = True):
        for item in self.items:
            painter.save()
            if item.is_shown is None:
                continue

            if item.is_shown == 2:
                painter.setPen(QColor(0, 0, 255))
            elif item.is_shown > 0:
                painter.setPen(QColor(0, 255, 0))
            else:
                painter.setPen(QColor(255, 0, 0))
                if not paint_hidden:
                    painter.restore()
                    continue
            rect = self.item_rect(item, scale=scale)
            painter.drawRect(rect)

            x = rect.x()
            y = rect.y()
            for character in self.characters_in_item(item):
                color = QColor(100, 150, 100, 128)  # RGB + Alpha (128 из 255 — это 50%)
                if character.color:
                    color = QColor(character.color.hex)
                    color.setAlpha(128)
                painter.setBrush(color)
                painter.setPen(color)
                triangle = QPolygonF([
                    QPointF(x, y),
                    QPointF(x+TRIANGLE_SIZE, y),
                    QPointF(x+TRIANGLE_SIZE/2, y+TRIANGLE_SIZE/1.4)
                ])
                x += TRIANGLE_SIZE
                painter.drawPolygon(triangle)
            painter.restore()

    def saveImage(self):
        if not self.pix_map_for_save.isNull():
            self.pix_map_for_save.save(self.file_name())
            self.map_image_saved.emit()

    def item_rect(self, item, scale=True) -> QRect:
        if item is None or self.original.width() == 0 or self.original.height() == 0:
            return QRect()
        if item.offsetX is None or item.offsetY is None or item.width is None or item.height is None:
            return QRect()
        w_aspect = self.size().width() / self.original.width()
        h_aspect = self.size().height() / self.original.height()
        if not scale:
            w_aspect, h_aspect = 1, 1
        return QRect(QPoint(int(item.offsetX * w_aspect),
                     int(item.offsetY * h_aspect)),
                     QSize(int(item.width * w_aspect),
                     int(item.height * h_aspect)))

    def set_file_path(self, file_path):
        if self.map is not None and self.session is not None:
            file_name = os.path.basename(file_path)
            if os.path.isfile(os.path.join(IMGS_DIR, file_name)):
                print(f"Warning: Файл c именем '{file_name}' уже существует в директории '{IMGS_DIR}'.")

            destination_path = os.path.join(IMGS_DIR, file_name)
            shutil.copy2(file_path, destination_path)

            self.map.filePath = file_name
            self.session.commit()
            self.set_map()

    def show_context_menu(self, pos, item):
        self.session = Session()
        menu = QMenu(self)
        action_show = QAction("Toggle", self)
        action_show.triggered.connect(lambda: self.toggle_item_visibility(item))
        menu.addAction(action_show)

        for character in self.session.query(PlayerCharacter).all():
            action = QAction(character.name, self)
            action.setCheckable(True)
            action.setChecked(self.character_presence(item, character))
            action.triggered.connect(lambda checked, c=character: self.toggle_character_presence(item, c))
            menu.addAction(action)
        menu.exec_(pos)

    def characters_in_item(self, item) -> list[PlayerCharacter]:
        self.session = Session()
        res = []
        for character in self.session.query(PlayerCharacter).all():
            if self.character_presence(item, character):
                res.append(character)
        return res

    def character_presence(self, item, character):
        pass

    def toggle_character_presence(self, item, character):
        pass
        # character.
        # self.session.commit()

    def toggle_item_visibility(self, item):
        if item.is_shown != 2:
            if item.is_shown > 0:
                item.is_shown = 0
            else:
                item.is_shown = 1
            self.session.commit()
            self.repaint()

    def add_item(self, name):
        pass

    def set_map(self):
        pass

    def file_name(self):
        return 'tmp'
