from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.location_npc_widget import LocationNpcWidget
from widgets.note_widget import NoteWidget
from common import AutoResizingListWidget, BaseListWidget


class EventListWidget(BaseListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def list_name(self) -> str:
        return 'Event List'
    
    def fill_first_line(self):
        super().fill_first_line()
        self.event_name = QLineEdit()
        self.first_line_layout.addWidget(self.event_name)

    def fill_head(self):
        pass
    
    def query_list(self) -> list:
        return self.session.query(Note).all()

    def widget_of(self, db_object) -> QWidget:
        return NoteWidget(db_object)

    def add_default_element(self):
        npc = Note()
        self.session.add(npc)
        self.session.commit()