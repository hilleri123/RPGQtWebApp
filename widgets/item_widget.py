from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QListWidgetItem, QInputDialog, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QSize
from scheme import *
from repositories import *
from common import AutoResizingTextEdit, AutoResizingListWidget, BaseListItemWidget, icons
from common.html_text_edit_widget import HtmlTextEdit
from .action_widget import ActionWidget
from dialogs import GameItemMoveDialog


class ItemWidget(BaseListItemWidget):
    def __init__(self, db_object: GameItem, parent=None):
        super().__init__(db_object, parent)

        self.xml_text = HtmlTextEdit()
        self.xml_text.setHtml(self.db_object.text)
        self.xml_text.textChanged.connect(self.on_save)
        self.base_layout.addWidget(self.xml_text)

        self.update_where()
        
    def fill_first_line(self):
        super().fill_first_line()
        self.where_label = QLabel()
        self.first_line_layout.addWidget(self.where_label)
        self.edit_item_button = QPushButton()
        self.edit_item_button.setIcon(icons.edit_icon())
        self.edit_item_button.setEnabled(IS_EDITABLE)
        self.edit_item_button.clicked.connect(self.on_edit_item)
        self.first_line_layout.addWidget(self.edit_item_button)
        self.move_item_button = QPushButton()
        self.move_item_button.setIcon(icons.move_icon())
        self.move_item_button.setEnabled(IS_EDITABLE)
        self.move_item_button.clicked.connect(self.on_move_item)
        self.first_line_layout.addWidget(self.move_item_button)

    def name(self) -> str:
        return self.db_object.name

    def update_where(self):
        where = self.session.query(WhereObject).filter(WhereObject.gameItemId == self.db_object.id).first()
        if where is None:
            icon = icons.error_icon()
        elif where.locationId is not None:
            icon = icons.location_icon()
        elif where.playerId is not None:
            icon = icons.player_icon()
        elif where.npcId is not None:
            icon = icons.npc_icon()
        else:
            icon = icons.error_icon()
        
        pixmap = icon.pixmap(QSize(16,16))  
        self.where_label.setPixmap(pixmap)
        self.changed.emit()

    def on_edit_item(self):
        pass

    def on_save(self):
        self.db_object.text = self.xml_text.toHtml()
        self.session.commit()
        super().on_save()

    def on_move_item(self):
        r = GameItemMoveDialog(self.db_object).exec()
        if r:
            self.update_where()
