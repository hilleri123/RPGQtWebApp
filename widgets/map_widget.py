from PyQt5.QtWidgets import QLabel, QWidget, QComboBox, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent
from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QSize
import typing
from scheme import *
from common import BaseMapLabel, BaseMapWidget


class MapLabel(BaseMapLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_map()

    def set_map(self):
        self.map = self.session.query(SceneMap).filter(SceneMap.isCurrent == True).first()
        if self.map is None:
            return
        self.items = self.session.query(Location).filter(Location.mapId == self.map.id).all()
        self.original = QPixmap(f'data/{self.map.filePath}')
        self.setPixmap(self.original)
        self.setScaledContents(True)


class MapWidget(BaseMapWidget):
    location_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mapSelector = QComboBox()
        for sceneMap in self.session.query(SceneMap).all():
            self.mapSelector.addItem(sceneMap.name, sceneMap.id)
        if self.mapLabel.map is not None:
            self.mapSelector.setCurrentText(self.mapLabel.map.name)
        self.mapSelector.activated.connect(self.on_select)
        self.button_layout.addWidget(self.mapSelector)

    def setup_label(self):
        self.mapLabel = MapLabel()
        self.mapLabel.item_clicked.connect(self.location_clicked)
        
    def on_select(self, idx):
        map_id = self.mapSelector.itemData(idx)
        self.set_current_map(map_id)
        self.location_clicked.emit(-1)

    def on_loc_update(self):
        self.mapLabel.set_map()
