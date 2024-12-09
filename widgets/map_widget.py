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
        self.session = Session()
        self.map = self.session.query(SceneMap).filter(SceneMap.isCurrent == True).first()
        if self.map is None:
            return
        self.items = self.session.query(Location).filter(Location.mapId == self.map.id).all()
        self.original = QPixmap(f'{IMGS_DIR}/{self.map.filePath}')
        self.setPixmap(self.original)
        self.setScaledContents(True)
        self.repaint()

    def add_item(self, name):
        tmp_loc = Location(name=name, offsetX=0, offsetY=0, width=100, height=100, mapId=self.map.id)
        self.session.add(tmp_loc)
        self.session.commit()
        self.set_map()
    
    def character_presence(self, item, character):
        if character.map_id != self.map.id:
            return False
        if character.location_id != item.id:
            return False
        return True

    def toggle_character_presence(self, item, character):
        character.map_id = self.map.id
        character.location_id = item.id
        self.session.commit()
        self.repaint()

    def file_name(self):
        return CURR_MAP_PATH
    
    def polygons(self) -> list[MapObjectPolygon]:
        return self.session.query(MapObjectPolygon).filter(MapObjectPolygon.map_id == self.map.id).all()


class MapWidget(BaseMapWidget):
    location_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mapSelector = QComboBox()
        self.button_layout.addWidget(self.mapSelector)
        self.resetup()

    def setup_label(self):
        self.mapLabel = MapLabel()
        self.mapLabel.item_clicked.connect(self.location_clicked)
        
    def on_select(self, idx):
        map_id = self.mapSelector.itemData(idx)
        self.set_current_map(map_id)
        self.location_clicked.emit(-1)

    def resetup(self):
        self.session = Session()
        for sceneMap in self.session.query(SceneMap).all():
            self.mapSelector.addItem(sceneMap.name, sceneMap.id)
        if self.mapLabel.map is not None:
            self.mapSelector.setCurrentText(self.mapLabel.map.name)
        self.mapSelector.activated.connect(self.on_select)
