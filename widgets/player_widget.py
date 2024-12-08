from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QDateTimeEdit, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *
from common import DateTimeEditWidget, AutoResizingListWidget
from dialogs import PlayerCharacterDialog


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
        tmp.addWidget(self.player_name_field)
        self.connection_label = QLabel()
        self.set_icon()
        tmp.addWidget(self.connection_label)
        self.lock_button = QPushButton()
        self.lock_button.setIcon(QIcon.fromTheme("system-lock-screen"))
        self.lock_button.clicked.connect(self.on_lock)
        tmp.addWidget(self.lock_button)
        self.edit_button = QPushButton()
        self.edit_button.setIcon(QIcon.fromTheme("preferences-system"))
        self.edit_button.setEnabled(IS_EDITABLE)
        self.edit_button.clicked.connect(self.on_edit)
        tmp.addWidget(self.edit_button)
        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon.fromTheme("list-remove"))
        self.delete_button.setEnabled(IS_EDITABLE)
        self.delete_button.clicked.connect(self.on_delete)
        tmp.addWidget(self.delete_button)
        self.base_layout.addLayout(tmp)
        self.datetime_edit = DateTimeEditWidget()
        self.datetime_edit.dateTimeChanged.connect(self.on_save)
        self.datetime_edit.need_to_sync.connect(self.on_sync)
        self.base_layout.addWidget(self.datetime_edit)
        
    def on_edit(self):
        dialog = PlayerCharacterDialog(character_id = self.player.id)
        dialog.exec()

    def on_delete(self):
        pass

    def on_save(self):
        self.player.time = self.datetime_edit.dateTime().toPyDateTime()
        self.session.commit()

    def on_lock(self):
        self.player.player_locked = not self.player.player_locked
        self.set_icon()
        self.session.commit()

    def set_icon(self):
        if self.player.player_locked:
            icon = QIcon.fromTheme("network-wired") 
        else:
            icon = QIcon.fromTheme("network-wireless")
        if self.player.address:
            self.connection_label.setToolTip(self.player.address)
        self.connection_label.setPixmap(icon.pixmap(16, 16))

    def update_datetime(self):
        if self.player.time:
            self.datetime_edit.setDateTime(self.player.time)

    def on_sync(self):
        self.session = Session()
        g_map = self.session.query(GlobalMap).first()
        if g_map is None:
            return
        if g_map.time:
            self.player.time = g_map.time
            self.session.commit()

            self.update_datetime()