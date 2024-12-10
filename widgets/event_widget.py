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

        self.shown_all = QCheckBox()
        self.shown_all.clicked.connect(self.set_all)
        self.first_line_layout.addWidget(self.shown_all)
        self.shown_combobox = CheckableComboBox(
            {p.id: p.name for p in self.players}, 
            json.loads(self.db_object.player_shown_json)
            )
        self.shown_combobox.state_chenged.connect(self.update_shown)
        self.first_line_layout.addWidget(self.shown_combobox)

    def on_save(self):
        ids = self.shown_combobox.get_checked_items_ids()
        self.db_object.player_shown_json = ids.__repr__()
        self.db_object.xml_text = self.note_text.toHtml()
        self.session.commit()
        super().on_save()

    def set_all(self):
        if self.shown_all.checkState() == Qt.Checked:
            state = Qt.Checked
        else:
            state = Qt.Unchecked
        self.shown_all.setCheckState(state)
        self.shown_combobox.set_all(state)
        self.on_save()

    def update_shown(self):
        ids = self.shown_combobox.get_checked_items_ids()
        if len(ids) == 0:
            self.shown_all.setCheckState(Qt.Unchecked)
        elif len(ids) == len(self.players):
            self.shown_all.setChecked(Qt.Checked)
        else:
            self.shown_all.setChecked(Qt.PartiallyChecked)
        self.on_save()


