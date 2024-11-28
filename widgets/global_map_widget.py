from PyQt5.QtWidgets import QLabel, QWidget, QComboBox, QVBoxLayout, QFileDialog, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent
from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QSize
import typing
from scheme import *
from common import BaseMapLabel, BaseMapWidget


class GlobalMapLabel(BaseMapLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_map()

    def set_map(self):
        self.map = self.session.query(GlobalMap).first()
        if self.map is None:
            self.map = GlobalMap(name="Base map")
            self.session.add(self.map)
            self.session.commit()
        self.items = self.session.query(SceneMap).all()
        self.original = QPixmap(f'data/imgs/{self.map.filePath}')
        self.setPixmap(self.original)
        self.setScaledContents(True)

    def add_item(self):
        tmp_map = SceneMap(name="", isCurrent=False, offsetX=0, offsetY=0, width=100, height=100)
        self.session.add(tmp_map)
        self.session.commit()
        self.set_map()



class GlobalMapWidget(BaseMapWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setup_label(self):
        self.mapLabel = GlobalMapLabel()
        self.mapLabel.item_clicked.connect(self.set_current_map)


