import os
import shutil
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QLabel, QWidget, QListWidget
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent
from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QSize, Qt


class AutoResizingTextEdit(QTextEdit):
    def __init__(self, max_height:int = None, parent=None):
        super().__init__(parent)
        self.max_height = max_height
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
        document.setTextWidth(self.viewport().width())
        height = margins.top() + document.size().height() + margins.bottom()
        # size = QSize(self.width(), int(height))
        # self.setMaximumSize(size)
        target_height = int(height+1)
        if self.max_height is not None:
            target_height = max(self.max_height, target_height)
        self.setMaximumHeight(target_height)
    
class AutoResizingListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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

    def setItemWidget(self, item, widget):
        super().setItemWidget(item, widget)
        self.auto_resize()
