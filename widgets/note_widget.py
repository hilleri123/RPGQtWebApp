from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QDateTimeEdit, QLineEdit, QTextEdit, 
    QListWidget, QPushButton, QHBoxLayout, QLabel, QComboBox, QCheckBox
)
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtCore import pyqtSignal, Qt
from scheme import *
from repositories import *
from common import AutoResizingTextEdit, DateTimeEditWidget, AutoResizingListWidget
from dialogs import PlayerCharacterDialog


class CheckableComboBox(QComboBox):
    state_chenged = pyqtSignal()

    def __init__(self, items_dict):
        super(CheckableComboBox, self).__init__()
        
        self.items_dict = items_dict
        self.model = QStandardItemModel()
        
        for item_id, item in items_dict.items():
            standard_item = QStandardItem(item)
            standard_item.setFlags(standard_item.flags() | Qt.ItemIsUserCheckable)
            standard_item.setData(Qt.Unchecked, Qt.CheckStateRole)
            self.model.appendRow(standard_item)
        
        self.setModel(self.model)
        self.model.itemChanged.connect(self.state_chenged)

    def get_checked_items_ids(self):
        checked_items_ids = []
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            if item.checkState() == Qt.Checked:
                # Получаем ключ по значению из словаря
                for key, value in self.items_dict.items():
                    if value == item.text():
                        checked_items_ids.append(key)
                        break
        return checked_items_ids
    
    def set_all(self, checked):
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            item.setData(checked, Qt.CheckStateRole)



class NoteWidget(QWidget):
    noteschange = pyqtSignal()
    deleted = pyqtSignal()

    def __init__(self, note: Note, parent=None):
        super().__init__(parent)
        self.session = Session()
        self.note = note
        self.players = self.session.query(PlayerCharacter).all()
        self.base_layout = QVBoxLayout(self)
        tmp = QHBoxLayout()
        self.shown_all = QCheckBox()
        self.shown_all.clicked.connect(self.set_all)
        tmp.addWidget(self.shown_all)
        self.shown_combobox = CheckableComboBox({p.id: p.name for p in self.players})
        self.shown_combobox.state_chenged.connect(self.update_shown)
        tmp.addWidget(self.shown_combobox)
        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon.fromTheme("list-remove"))
        self.delete_button.setEnabled(IS_EDITABLE)
        self.delete_button.clicked.connect(self.on_delete)
        tmp.addWidget(self.delete_button)
        self.base_layout.addLayout(tmp)
        self.note_text = AutoResizingTextEdit()
        self.note_text.setHtml(note.xml_text)
        if not IS_EDITABLE:
            self.note_text.setReadOnly(True)
        self.note_text.textChanged.connect(self.on_save)
        self.base_layout.addWidget(self.note_text)
        
    
    def on_delete(self):
        # TODO пофиксить
        self.session.delete(self.note)
        self.session.commit()
        self.deleted.emit()

    def on_save(self):
        ids = self.shown_combobox.get_checked_items_ids()
        self.note.player_shown_json = ids.__repr__()
        self.note.xml_text = self.note_text.toHtml()
        self.session.commit()

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


