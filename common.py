from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QLabel, QWidget, QListWidget
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
        if item is None:
            return QRect()
        w_aspect = self.size().width() / self.original.width()
        h_aspect = self.size().height() / self.original.height()
        return QRect(QPoint(int(item.offsetX * w_aspect),
                     int(item.offsetY * h_aspect)),
                     QSize(int(item.width * w_aspect),
                     int(item.height * h_aspect)))
