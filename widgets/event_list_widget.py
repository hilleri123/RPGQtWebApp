from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.location_npc_widget import LocationNpcWidget
from widgets.event_widget import EventWidget
from common import AutoResizingListWidget, BaseListWidget
from sqlalchemy import and_
from pyqttoast import Toast, ToastPreset, ToastPosition


class EventListWidget(BaseListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.time = None
        self.set_time()

    def set_time(self):
        g_map = self.session.query(GlobalMap).first()
        if g_map is None:
            return
        self.toast(self.time, g_map.time)
        self.time = g_map.time
        self.fill_list()

    def list_name(self) -> str:
        return 'Event List'
    
    def fill_first_line(self):
        super().fill_first_line()

    def fill_head(self):
        pass
    
    def query_list(self) -> list:
        try:
            if self.time is None:
                return []
        except AttributeError:
            return []
        
        active_events = []
        future_events = []
        past_events = []
        for event in self.session.query(GameEvent).all():
            if (event.start_time is None or event.start_time <= self.time) and (event.end_time is None or event.end_time >= self.time):
                active_events.append(event)   # Действующие события
            elif event.start_time is not None and event.start_time > self.time:
                future_events.append(event)   # Будущие события
            else:
                past_events.append(event)     

        return active_events + future_events + past_events

    def widget_of(self, db_object) -> QWidget:
        return EventWidget(db_object)

    def add_default_element(self):
        event = GameEvent()
        self.session.add(event)
        self.session.commit()

    def toast(self, from_dt, to_dt):
        if from_dt is None or to_dt is None:
            return
        events = self.session.query(GameEvent).filter(
            and_(GameEvent.start_time > from_dt, GameEvent.start_time <= to_dt)
            ).all()
        if len(events) == 0:
            return
        event_txt = [self.to_plain_text(event.xml_text) for event in events]

        toast = Toast(None)
        Toast.setPosition(ToastPosition.BOTTOM_RIGHT) 
        toast.setDuration(5000)
        toast.setTitle(f"Событий {len(events)}") 
        toast.setText('\n'.join(event_txt))
        toast.applyPreset(ToastPreset.SUCCESS)
        toast.show()

    def to_plain_text(self, xml):
        tmp = QTextEdit()
        tmp.setHtml(xml)
        txt = tmp.toPlainText()
        tmp.deleteLater()
        return txt
