from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.location_npc_widget import LocationNpcWidget
from widgets.event_widget import EventWidget
from common import AutoResizingListWidget, BaseListWidget


class EventListWidget(BaseListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.time = None
        self.set_time()

    def set_time(self):
        g_map = self.session.query(GlobalMap).first()
        if g_map is None:
            return
        self.time = g_map.time

    def list_name(self) -> str:
        return 'Event List'
    
    def fill_first_line(self):
        super().fill_first_line()

    def fill_head(self):
        pass
    
    def query_list(self) -> list:
        active_events = []
        future_events = []
        past_events = []
        for event in self.session.query(GameEvent).all():
            if event.happend:
                past_events.append(event)
                continue
            
            s_left, e_left = False, False
            if event.start_time is not None:
                pass
                # s_left = 

        return active_events + future_events + past_events

    def widget_of(self, db_object) -> QWidget:
        return EventWidget(db_object)

    def add_default_element(self):
        event = GameEvent()
        self.session.add(event)
        self.session.commit()