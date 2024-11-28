from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *
from common import AutoResizingTextEdit, AutoResizingListWidget


class NpcWidget(QWidget):
    def __init__(self, npc: NPC, parent=None, **args):
        super().__init__(parent)
        self.session = Session()
        self.npc = npc
        self.base_layout = QVBoxLayout(self)
        self.setup(**args)
        self.add_lists(**args)
        

    def setup(self, **args):
        dialogs = check_marks_in_condition(
            self.session.query(GameCondition).filter(
                GameCondition.playerActionId != None,
                GameCondition.locationId == None,
                GameCondition.npcId == self.npc.id
            ).all()
        )

        # Формы для полей
        tmp = QHBoxLayout()
        self.npc_name_field = QLineEdit()  # Поле для имени NPC
        self.npc_name_field.setText(self.npc.name)
        self.npc_name_field.setReadOnly(True)
        tmp.addWidget(self.npc_name_field)
        self.edit_npc_button = QPushButton()
        self.edit_npc_button.setIcon(QIcon.fromTheme("preferences-system"))
        self.edit_npc_button.setEnabled(IS_EDITABLE)
        self.edit_npc_button.clicked.connect(self.on_edit_npc)
        tmp.addWidget(self.edit_npc_button)
        self.add_dialog_button = QPushButton()
        self.add_dialog_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_dialog_button.setEnabled(IS_EDITABLE)
        self.add_dialog_button.clicked.connect(self.on_add_dialog)
        tmp.addWidget(self.add_dialog_button)
        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon.fromTheme("list-remove"))
        self.delete_button.setEnabled(IS_EDITABLE)
        self.delete_button.clicked.connect(self.on_delete)
        tmp.addWidget(self.delete_button)
        self.base_layout.addLayout(tmp)


    def add_lists(self, **args):
        self.dialogs_list = AutoResizingListWidget()
        self.base_layout.addWidget(QLabel("Общие диалоги:"))
        self.base_layout.addWidget(self.dialogs_list)


    def on_edit_npc(self):
        pass #TODO


    def on_add_dialog(self):
        pass #TODO


    def on_delete(self):
        pass #TODO

