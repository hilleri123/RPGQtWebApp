from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QListWidgetItem, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *
from common import AutoResizingTextEdit, AutoResizingListWidget
from .action_widget import ActionWidget


class NpcWidget(QWidget):
    deleted = pyqtSignal()

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
        self.dialogs = []
        self.dialogs_list = AutoResizingListWidget()
        self.base_layout.addWidget(QLabel("Общие диалоги:"))
        self.base_layout.addWidget(self.dialogs_list)
        self.dialogs_fill()


    def dialogs_fill(self):
        self.dialogs_list.clear()

        self.dialogs = check_marks_in_condition(
            self.session.query(GameCondition).filter(
                GameCondition.playerActionId != None,
                GameCondition.locationId == None,
                GameCondition.npcId == self.npc.id
            ).all()
        )

        for dialog in self.dialogs:
            item = QListWidgetItem(self.dialogs_list)
            widget = ActionWidget(action_id=dialog.playerActionId)
            widget.deleted.connect(self.dialogs_fill)
            self.dialogs_list.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

    def on_edit_npc(self):
        pass #TODO


    def on_add_dialog(self):
        a = PlayerAction()
        self.session.add(a)
        self.session.commit()
        c = GameCondition(
            playerActionId=a.id,
            npcId = self.npc.id
            )
        self.session.add(c)
        self.session.commit()
        
        self.dialogs_fill()


    def on_delete(self):
        # TODO пофиксить
        self.session.delete(self.npc)
        self.session.commit()

        self.deleted.emit()

