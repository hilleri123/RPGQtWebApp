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
        self.session = Session()
        self.map = self.session.query(GlobalMap).first()
        if self.map is None:
            self.map = GlobalMap(name="Base map")
            self.session.add(self.map)
            self.session.commit()
        self.items = self.session.query(SceneMap).all()
        self.original = QPixmap(f'{IMGS_DIR}/{self.map.filePath}')
        self.setPixmap(self.original)
        self.setScaledContents(True)
        self.repaint()

    def add_item(self, name):
        tmp_map = SceneMap(name=name, isCurrent=False, offsetX=0, offsetY=0, width=100, height=100)
        self.session.add(tmp_map)
        self.session.commit()
        self.set_map()
        
    def character_presence(self, item, character):
        if character.map_id != item.id:
            return False
        return True

    def toggle_character_presence(self, item, character):
        if character.map_id == item.id:
            return 
        character.map_id = item.id
        character.location_id = None
        self.session.commit()
        self.repaint()
    
    def file_name(self):
        return GLOBAL_MAP_PATH
    
    def polygons(self) -> list[MapObjectPolygon]:
        return self.session.query(MapObjectPolygon).filter(MapObjectPolygon.global_map_id == self.map.id).all()


class GlobalMapWidget(BaseMapWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.map_object_clicked.connect(self.set_current_map)
    
    def construct_label(self):
        return GlobalMapLabel()

