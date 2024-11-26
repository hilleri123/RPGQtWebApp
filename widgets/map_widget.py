from PyQt5.QtWidgets import QLabel, QWidget, QComboBox, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent
from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QSize
import typing
from scheme import *


class MapLabel(QLabel):
    location_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Session()
        self.original = QPixmap()
        self.map = None
        self.location_list = []
        self.set_map()

    def set_map(self):
        self.map = self.session.query(SceneMap).filter(SceneMap.isCurrent == True).first()
        if self.map is None:
            return
        print(self.map.name, self.map.filePath)
        self.location_list = self.session.query(Location).filter(Location.mapId == self.map.id).all()
        print(self.location_list)
        self.original = QPixmap(f'data/{self.map.filePath}')
        self.setPixmap(self.original)
        self.setScaledContents(True)

    def mousePressEvent(self, ev: typing.Optional[QMouseEvent]) -> None:
        if ev is None:
            return
        pos = ev.pos()

        for location in self.location_list:
            if self.location_rect(location).contains(pos):
                self.location_clicked.emit(location.id)
                break

    def paintEvent(self, a0: typing.Optional[QPaintEvent]) -> None:
        super().paintEvent(a0)
        painter = QPainter(self)
        painter.setPen(QColor(255, 0, 0))

        for location in self.location_list:
            painter.drawRect(self.location_rect(location))

    def location_rect(self, location: Location) -> QRect:
        if location is None:
            return QRect()
        w_aspect = self.size().width() / self.original.width()
        h_aspect = self.size().height() / self.original.height()
        return QRect(QPoint(int(location.offsetX * w_aspect),
                     int(location.offsetY * h_aspect)),
                     QSize(int(location.width * w_aspect),
                     int(location.height * h_aspect)))


class MapWidget(QWidget):
    location_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumSize(700, 500)
        self.session = Session()
        self.setLayout(QVBoxLayout())
        self.mapLabel = MapLabel()
        self.mapLabel.location_clicked.connect(self.location_clicked)
        self.layout().addWidget(self.mapLabel)
        self.mapSelector = QComboBox()
        for sceneMap in self.session.query(SceneMap).all():
            self.mapSelector.addItem(sceneMap.name, sceneMap.id)
        if self.mapLabel.map is not None:
            self.mapSelector.setCurrentText(self.mapLabel.map.name)
        self.mapSelector.activated.connect(self.on_select)
        self.layout().addWidget(self.mapSelector)

    def on_select(self, idx):
        map_id = self.mapSelector.itemData(idx)
        print(idx, map_id)
        record_to_update = self.session.query(SceneMap) \
            .filter(SceneMap.isCurrent == True).first()
        if record_to_update is not None:
            record_to_update.isCurrent = False
        print(record_to_update.name, record_to_update.isCurrent)
        record_to_update = self.session.query(SceneMap) \
            .filter(SceneMap.id == map_id).first()
        if record_to_update is not None:
            record_to_update.isCurrent = True
        print(record_to_update.name, record_to_update.isCurrent)
        self.session.commit()
        self.mapLabel.set_map()
        self.location_clicked.emit(-1)
