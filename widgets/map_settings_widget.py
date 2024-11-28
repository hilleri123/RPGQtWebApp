from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.location_npc_widget import LocationNpcWidget
from common import BaseMapObject, AutoResizingTextEdit, AutoResizingListWidget


class MapSettingsWidget(BaseMapObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.on_map_selected()

    def on_map_selected(self) -> None:
        self.session = Session()
        self.object = self.session.query(SceneMap).filter(SceneMap.isCurrent == True).first()
        if self.object is None:
            return

        self.setup_map_object()
