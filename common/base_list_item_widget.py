from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QDateTimeEdit, QLineEdit, QTextEdit, 
    QListWidget, QPushButton, QHBoxLayout, QLabel, QComboBox, QCheckBox
)
from PyQt5.QtGui import QIcon, QStandardItem,  QStandardItemModel
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from scheme import *
from .icons import delete_icon
import json



class BaseListItemWidget(QWidget):
    changed = pyqtSignal()
    deleted = pyqtSignal()
    set_hint = pyqtSignal(QSize)

    def __init__(self, db_object, parent=None):
        super().__init__(parent)
        self.session = Session()
        self.db_object = db_object
        self.base_layout = QVBoxLayout(self)
        self.first_line_layout = QHBoxLayout()
        self.base_layout.addLayout(self.first_line_layout)
        self.item_name_field = QLineEdit()
        self.item_name_field.setText(self.name())
        self.item_name_field.textChanged.connect(self.on_save)
        if self.name() is not None:
            self.first_line_layout.addWidget(self.item_name_field)
        self.fill_first_line()
        self.delete_button = QPushButton()
        self.delete_button.setIcon(delete_icon())
        self.delete_button.setEnabled(IS_EDITABLE)
        self.delete_button.clicked.connect(self.on_delete)
        self.first_line_layout.addWidget(self.delete_button)

    def fill_first_line(self):
        pass

    def name(self) -> str:
        return ''    
    
    def on_delete(self):
        self.session.delete(self.db_object)
        self.session.commit()
        self.deleted.emit()

    def on_save(self):
        try:
            self.db_object.name = self.item_name_field.text()
        except:
            pass
        self.session.commit()
        self.set_hint.emit(self.sizeHint())
        self.changed.emit()

    def is_hidden(self):
        return False
