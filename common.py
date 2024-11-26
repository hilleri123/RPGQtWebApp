from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget, QListWidget
from PyQt5.QtCore import QSize, Qt
# from PyQt5.QtGui import Qt

class AutoResizingTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.textChanged.connect(self.updateGeometry)

    def sizeHint(self) -> QSize:
        document = self.document()
        margins = self.contentsMargins()
        document.setTextWidth(self.viewport().width())
        height = margins.top() + document.size().height() + margins.bottom()
        size = QSize(self.width(), int(height))
        self.setFixedSize(size)

        return size
    
class AutoResizingListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.itemChanged.connect(self.updateGeometry)

    def sizeHint(self) -> QSize:
        margins = self.contentsMargins()
        frame_width = self.frameWidth()
        total_height = 0
        for index in range(self.count()):
            item = self.item(index)
            total_height += self.visualItemRect(item).height()
        total_height += margins.top() + margins.bottom() + frame_width * 2
        width = self.sizeHintForColumn(0) + margins.left() + margins.right() + frame_width * 2
        size = QSize(width, total_height)
        self.setFixedSize(size)

        return size


