import os
import shutil
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QLabel, QWidget, QListWidget
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent
from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QSize, Qt, QTimer

from .base_list_item_widget import BaseListItemWidget

class AutoResizingTextEdit(QTextEdit):
    def __init__(self, max_height:int = None, is_fixed=True, parent=None):
        super().__init__(parent)
        self.max_height = max_height
        self.is_fixed = is_fixed
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.previous_width = 0

        self.textChanged.connect(self.auto_resize)
        self.auto_resize()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        current_width = self.width()
        if current_width != self.previous_width:
            self.previous_width = current_width
            self.auto_resize()

    def auto_resize(self):
        document = self.document()
        margins = self.contentsMargins()
        document.setTextWidth(self.viewport().width()-margins.left()-margins.right())
        height = margins.top() + document.size().height() + margins.bottom()
        # size = QSize(self.width(), int(height))
        # self.setMaximumSize(size)
        target_height = int(height+1)
        if self.max_height is not None:
            target_height = min(self.max_height, target_height)
        if self.is_fixed:
            self.setFixedHeight(target_height)
        else:
            self.setMaximumHeight(target_height)
        self.repaint()
    
class AutoResizingListWidget(QListWidget):
    def __init__(self, shown_elemets:int = 1, max_height:int = 2000, parent=None):
        super().__init__(parent)
        self.max_height = max_height
        self.shown_elemets = shown_elemets
        self.previous_width = 0

        self.itemChanged.connect(self.auto_resize)
        self.auto_resize()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        current_width = self.width()
        if current_width != self.previous_width:
            self.previous_width = current_width
            self.auto_resize()

    def auto_resize(self):
        self.updateGeometries()
        margins = self.contentsMargins()
        frame_width = self.frameWidth()
        total_height = 0
        min_height = 0
        for index in range(self.count()):
            item = self.item(index)
            total_height += self.visualItemRect(item).height()
            if index < self.shown_elemets:
                min_height += self.visualItemRect(item).height()
        total_height += margins.top() + margins.bottom() + frame_width * 2
        min_height += margins.top() + margins.bottom() + frame_width * 2
        # width = self.sizeHintForColumn(0) + margins.left() + margins.right() + frame_width * 2
        # size = QSize(width, total_height)
        # self.setMaximumSize(size)
        target_height = int(total_height+1)
        if self.max_height is not None:
            target_height = min(self.max_height, target_height)
        # self.setFixedHeight(target_height)
        self.setMinimumHeight(min_height)
        self.setMaximumHeight(target_height)
        # if self.parent():
        #     self.parent().updateGeometry()
        #     if self.parent().parent():
        #         self.parent().parent().updateGeometry()
        # print('?', target_height)
        self.repaint()

    def setItemWidget(self, item, widget):
        super().setItemWidget(item, widget)
        if self.count() % 2:
            item.setBackground(QColor(100,100,100,30))
        if issubclass(type(widget), BaseListItemWidget):
            widget.set_hint.connect(item.setSizeHint)
        self.auto_resize()
