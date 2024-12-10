from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QMessageBox, QDateTimeEdit, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *
from common import DateTimeEditWidget, BaseListItemWidget, icons
from dialogs import PlayerCharacterDialog


class PlayerWidget(BaseListItemWidget):
    def __init__(self, player: PlayerCharacter, parent=None):
        super().__init__(player, parent)

        self.datetime_edit = DateTimeEditWidget()
        self.datetime_edit.dateTimeChanged.connect(self.on_save)
        self.datetime_edit.need_to_sync.connect(self.on_sync)
        self.base_layout.addWidget(self.datetime_edit)
        
    def fill_first_line(self):
        self.connection_label = QLabel()
        self.set_icon()
        self.first_line_layout.addWidget(self.connection_label)
        self.lock_button = QPushButton()
        self.lock_button.setIcon(icons.lock_icon())
        self.lock_button.clicked.connect(self.on_lock)
        self.first_line_layout.addWidget(self.lock_button)
        self.edit_button = QPushButton()
        self.edit_button.setIcon(icons.edit_icon())
        self.edit_button.setEnabled(IS_EDITABLE)
        self.edit_button.clicked.connect(self.on_edit)
        self.first_line_layout.addWidget(self.edit_button)

    def name(self) -> str:
        return self.db_object.name

    def on_edit(self):
        dialog = PlayerCharacterDialog(character_id = self.db_object.id)
        dialog.exec()

    def on_delete(self):
        confirm_dialog = QMessageBox(self)
        confirm_dialog.setWindowTitle("Подтверждение удаления")
        confirm_dialog.setText(f"Вы уверены, что хотите удалить {self.name()}?")
        confirm_dialog.setIcon(QMessageBox.Warning)
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = confirm_dialog.exec_()
        if result == QMessageBox.Yes:
            super().on_delete()


    def on_save(self):
        self.db_object.time = self.datetime_edit.dateTime().toPyDateTime()
        self.session.commit()
        super().on_save()

    def on_lock(self):
        self.db_object.player_locked = not self.db_object.player_locked
        self.set_icon()
        self.session.commit()

    def set_icon(self):
        if self.db_object.player_locked:
            icon = icons.connect_icon()
        else:
            icon = icons.lost_icon()
        if self.db_object.address:
            self.connection_label.setToolTip(self.db_object.address)
        self.connection_label.setPixmap(icon.pixmap(16, 16))

    def update_datetime(self):
        if self.db_object.time:
            self.datetime_edit.setDateTime(self.db_object.time)

    def on_sync(self):
        self.session = Session()
        g_map = self.session.query(GlobalMap).first()
        if g_map is None:
            return
        if g_map.time:
            self.db_object.time = g_map.time
            self.session.commit()

            self.update_datetime()