from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.location_npc_widget import LocationNpcWidget
from widgets.item_widget import ItemWidget
from common import BaseListWidget, HtmlTextEdit, AutoResizingListWidget


class ItemListWidget(BaseListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Session()
        self.location_id = None


    def list_name(self) -> str:
        return 'Item list'

    def fill_first_line(self):
        super().fill_first_line()
        self.item_name = QLineEdit()
        self.first_line_layout.addWidget(self.item_name)
        self.location_label = QLabel()
        self.first_line_layout.addWidget(self.location_label)

    def fill_head(self):
        super().fill_head()
        self.item_description = HtmlTextEdit()
        self.base_layout.addWidget(self.item_description)

    def set_location(self, location_id):
        location = self.session.query(Location).get(location_id)
        if location is None:
            return
        self.location_id = location_id
        self.location_label.setText(f"Location: {location.name}")
    
    def query_list(self) -> list:
        return self.session.query(GameItem).all()
    
    def widget_of(self, db_object) -> QWidget:
        return ItemWidget(db_object)

    def add_default_element(self):
        item = GameItem(name=self.item_name.text(), text=self.item_description.toHtml())
        self.session.add(item)
        self.session.commit()
        if self.location_id is not None:
            where = self.session.query(WhereObject).filter(WhereObject.gameItemId == item.id).first()
            if where is None:
                where = WhereObject(gameItemId=item.id)
                self.session.add(where)
            where.locationId = self.location_id
            where.playerId = None
            where.npcId = None
            self.session.commit()