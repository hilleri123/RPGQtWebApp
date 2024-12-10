from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.player_widget import PlayerWidget
from common import AutoResizingListWidget, BaseListWidget


class PlayerListWidget(BaseListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def list_name(self) -> str:
        return 'Player List'

    def fill_first_line(self):
        super().fill_first_line()
        self.player_name = QLineEdit()
        self.first_line_layout.addWidget(self.player_name)

    def fill_head(self):
        super().fill_head()

    def query_list(self) -> list:
        return self.session.query(PlayerCharacter).all()

    def widget_of(self, db_object) -> QWidget:
        return PlayerWidget(db_object)

    def add_default_element(self):
        player = PlayerCharacter(name=self.player_name.text())
        self.session.add(player)
        self.session.commit()

    def update_connections(self):
        for i in range(self.item_list.count()):
            item = self.item_list.item(i)
            widget = self.item_list.itemWidget(item)
            if widget:
                widget.set_icon()
    
    def on_datetime_changed(self):
        for i in range(self.item_list.count()):
            item = self.item_list.item(i)
            widget = self.item_list.itemWidget(item)
            if widget:
                widget.update_datetime()
