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
        
    def fill_first_line(self):
        super().fill_first_line()
        self.players = self.session.query(PlayerCharacter).all()

        self.happend = QCheckBox()
        self.happend.clicked.connect(self.on_save)
        self.first_line_layout.addWidget(self.happend)

    def on_save(self):
        self.db_object.happend = self.happend.isChecked()
        self.db_object.xml_text = self.note_text.toHtml()
        self.session.commit()
        super().on_save()


