from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.location_npc_widget import LocationNpcWidget
from widgets.npc_widget import NpcWidget
from common import AutoResizingListWidget, BaseListWidget


class NpcListWidget(BaseListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def list_name(self) -> str:
        return 'list'

    def fill_first_line(self):
        super().fill_first_line()
        self.npc_name = QLineEdit()
        self.first_line_layout.addWidget(self.npc_name)

    def fill_head(self):
        super().fill_head()

    def query_list(self) -> list:
        return self.session.query(NPC).all()

    def widget_of(self, db_object) -> QWidget:
        return NpcWidget(db_object)
    
    def add_default_element(self):
        npc = NPC(name=self.npc_name.text())
        self.session.add(npc)
        self.session.commit()