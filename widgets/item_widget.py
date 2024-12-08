from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QListWidgetItem, QInputDialog, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QSize
from scheme import *
from repositories import *
from common import AutoResizingTextEdit, AutoResizingListWidget, icons
from common.html_text_edit_widget import HtmlTextEdit
from .action_widget import ActionWidget
from dialogs import GameItemMoveDialog


class ItemWidget(QWidget):
    item_moved = pyqtSignal()
    deleted = pyqtSignal()

    def __init__(self, item: GameItem, parent=None, **args):
        super().__init__(parent)
        self.session = Session()
        self.item = item
        self.base_layout = QVBoxLayout(self)
        
        tmp = QHBoxLayout()
        self.item_name_field = QLineEdit()  # Поле для имени NPC
        self.item_name_field.setText(self.item.name)
        self.item_name_field.setReadOnly(True)
        tmp.addWidget(self.item_name_field)
        self.where_label = QLabel()
        tmp.addWidget(self.where_label)
        self.edit_item_button = QPushButton()
        self.edit_item_button.setIcon(icons.edit_icon())
        self.edit_item_button.setEnabled(IS_EDITABLE)
        self.edit_item_button.clicked.connect(self.on_edit_item)
        tmp.addWidget(self.edit_item_button)
        self.move_item_button = QPushButton()
        self.move_item_button.setIcon(icons.move_icon())
        self.move_item_button.setEnabled(IS_EDITABLE)
        self.move_item_button.clicked.connect(self.on_move_item)
        tmp.addWidget(self.move_item_button)
        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon.fromTheme("list-remove"))
        self.delete_button.setEnabled(IS_EDITABLE)
        self.delete_button.clicked.connect(self.on_delete)
        tmp.addWidget(self.delete_button)
        self.base_layout.addLayout(tmp)

        self.xml_text = HtmlTextEdit()
        self.xml_text.setHtml(self.item.text)
        self.xml_text.textChanged.connect(self.on_save)
        self.base_layout.addWidget(self.xml_text)

        self.update_where()

    def update_where(self):
        where = self.session.query(WhereObject).filter(WhereObject.gameItemId == self.item.id).first()
        if where is None:
            icon = QIcon.fromTheme("dialog-error")
        elif where.locationId is not None:
            icon = QIcon.fromTheme("go-home")
        elif where.playerId is not None:
            icon = QIcon.fromTheme("user-available")
        elif where.npcId is not None:
            icon = QIcon.fromTheme("user-offline")
        else:
            icon = QIcon.fromTheme("dialog-error")
        
        pixmap = icon.pixmap(QSize(16,16))  
        self.where_label.setPixmap(pixmap)
        self.item_moved.emit()

    def on_edit_item(self):
        pass
    #     text, ok = QInputDialog.getMultiLineText(
    #         None, "Введите HTML", "HTML код:", "<html><body></body></html>"
    #     )
    #     if ok:
    #         self.item.text = text
    #         self.session.commit()

    def on_save(self):
        self.item.text = self.xml_text.toHtml()
        self.session.commit()

    def on_delete(self):
        self.session.delete(self.item)
        self.session.commit()

        self.deleted.emit()

    def on_move_item(self):
        r = GameItemMoveDialog(self.item).exec()
        if r:
            self.update_where()
