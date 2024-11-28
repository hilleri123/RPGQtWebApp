from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QDateTimeEdit, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *
from common import AutoResizingTextEdit, AutoResizingListWidget


class PlayerWidget(QWidget):
    def __init__(self, player: PlayerCharacter, parent=None):
        super().__init__(parent)
        self.session = Session()
        self.player = player
        self.base_layout = QVBoxLayout(self)
        tmp = QHBoxLayout()
        self.player_name_field = QLineEdit()  # Поле для имени NPC
        self.player_name_field.setText(self.player.name)
        self.player_name_field.setReadOnly(True)
        tmp.addWidget(self.npc_naplayer_name_fieldme_field)
        self.edit_npc_button = QPushButton()
        self.edit_npc_button.setIcon(QIcon.fromTheme("preferences-system"))
        self.edit_npc_button.setEnabled(IS_EDITABLE)
        self.edit_npc_button.clicked.connect(self.on_edit)
        tmp.addWidget(self.edit_npc_button)
        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon.fromTheme("list-remove"))
        self.delete_button.setEnabled(IS_EDITABLE)
        self.delete_button.clicked.connect(self.on_delete)
        tmp.addWidget(self.delete_button)
        self.base_layout.addLayout(tmp)
        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.dateTimeChanged.connect(self.on_save)
        self.base_layout.addWidget(self.datetime_edit)
        
    def on_edit(self):
        pass

    def on_delete(self):
        pass

    def on_save(self):
        self.player.time = self.datetime_edit.dateTime()
        self.session.commit()
