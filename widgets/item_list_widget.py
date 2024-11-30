from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.location_npc_widget import LocationNpcWidget
from widgets.item_widget import ItemWidget
from common import BaseMapObject, AutoResizingTextEdit, AutoResizingListWidget


class ItemListWidget(QWidget):
    item_list_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Session()
        self.location_id = None

        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)

        tmp_layout = QHBoxLayout()
        self.base_layout.addLayout(tmp_layout)
        tmp_layout.addWidget(QLabel("Item list:")) 
        self.item_name = QLineEdit()
        tmp_layout.addWidget(self.item_name)
        self.add_item_button = QPushButton()
        self.add_item_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_item_button.clicked.connect(self.on_add_item)
        tmp_layout.addWidget(self.add_item_button)
        self.location_label = QLabel()
        tmp_layout.addWidget(self.location_label)
        self.item_description = AutoResizingTextEdit()
        self.base_layout.addWidget(self.item_description)

        self.item_list = AutoResizingListWidget()
        self.base_layout.addWidget(self.item_list)
        self.fill_items()

    def set_location(self, location_id):
        location = self.session.query(Location).get(location_id)
        if location is None:
            return
        self.location_id = location_id
        self.location_label.setText(f"Location: {location.name}")

    def fill_items(self):
        self.item_list.clear()
        self.session = Session()

        item_list = self.session.query(GameItem).all()
        for game_item in item_list:
            item = QListWidgetItem(self.item_list)
            widget = ItemWidget(item=game_item)
            widget.deleted.connect(self.fill_items)
            self.item_list.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

    def on_add_item(self):
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
        self.fill_items()
        self.item_list_changed.emit()