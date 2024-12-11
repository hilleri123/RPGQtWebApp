from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QDateTimeEdit, QLineEdit, QTextEdit, 
    QListWidget, QPushButton, QHBoxLayout, QLabel, QComboBox, QCheckBox
)
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtCore import pyqtSignal, Qt
from scheme import *
from repositories import *
from common import HtmlTextEdit, DateTimeEditWidget, BaseListItemWidget
from dialogs import PlayerCharacterDialog
import json



class EventWidget(BaseListItemWidget):
    def __init__(self, db_object, parent=None):
        super().__init__(db_object, parent)
        self.note_text = HtmlTextEdit()
        self.note_text.setHtml(db_object.xml_text)
        if not IS_EDITABLE:
            self.note_text.setReadOnly(True)
        self.note_text.textChanged.connect(self.on_save)
        self.base_layout.addWidget(self.note_text)

        self.on_save()
        
    def fill_first_line(self):
        super().fill_first_line()
        self.start = DateTimeEditWidget()
        self.start.setDateTime(self.db_object.start_time)
        self.first_line_layout.addWidget(self.start)
        self.end = DateTimeEditWidget()
        self.end.setDateTime(self.db_object.end_time)
        self.first_line_layout.addWidget(self.end)

        self.happend = QCheckBox()
        self.first_line_layout.addWidget(self.happend)

        g_map = self.session.query(GlobalMap).first()
        if g_map is None:
            return
        if g_map.start_time is None:
            return
        if self.db_object.start_time is None:
            self.start.setDateTime(g_map.start_time)
        if self.db_object.end_time is None:
            self.end.setDateTime(g_map.start_time)

        self.start.dateTimeChanged.connect(self.on_save)
        self.end.dateTimeChanged.connect(self.on_save)
        self.happend.clicked.connect(self.on_save)


    def on_save(self):
        self.db_object.happend = self.happend.isChecked()
        self.db_object.xml_text = self.note_text.toHtml()
        self.db_object.start_time = self.start.dateTime().toPyDateTime()
        self.db_object.end_time = self.end.dateTime().toPyDateTime()
        self.session.commit()
        super().on_save()


