from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidgetItem, QFormLayout, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *
from common import AutoResizingTextEdit, AutoResizingListWidget
from .npc_widget import NpcWidget
from .action_widget import ActionWidget


class LocationNpcWidget(NpcWidget):
    def __init__(self, npc: NPC, appearance: list[str] = None, location: Location = None, parent=None):
        super().__init__(npc, parent, appearance=appearance, location=location)

    def setup(self, appearance, location):
        super().setup()
        self.location = location
        self.loc_dialogs = []
        # TODO редактировать appearance
        if appearance is not None:
            self.appearance_field = AutoResizingTextEdit()  # Поле для списка внешностей (appearance)
            self.appearance_field.setText('; '.join(appearance))
            self.appearance_field.setReadOnly(True)
            self.base_layout.addWidget(self.appearance_field)

        self.loc_dialogs_list = AutoResizingListWidget()  # Список локальных диалогов
        
        self.labels.append(QLabel("Локальные диалоги:"))
        self.base_layout.addWidget(self.labels[-1])
        self.base_layout.addWidget(self.loc_dialogs_list)

        self.loc_dialogs_fill()


    def loc_dialogs_fill(self):
        self.loc_dialogs_list.clear()

        if self.location is None:
            return
        self.loc_dialogs = check_marks_in_condition(
            self.session.query(GameCondition).filter(
                GameCondition.playerActionId != None,
                GameCondition.locationId == self.location.id,
                GameCondition.npcId == self.db_object.id
            ).all()
        )

        for loc_dialog in self.loc_dialogs:
            item = QListWidgetItem(self.loc_dialogs_list)
            widget = ActionWidget(action_id=loc_dialog.playerActionId)
            widget.deleted.connect(self.loc_dialogs_fill)
            self.loc_dialogs_list.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

    def on_edit_npc(self):
        if self.dialogs_list.isHidden() or self.loc_dialogs_list.isHidden():
            self.dialogs_list.show()
            self.loc_dialogs_list.show()
            for l in self.labels:
                l.show()
        else:
            self.dialogs_list.hide()
            self.loc_dialogs_list.hide()
            for l in self.labels:
                l.hide()


    def on_add_dialog(self):
        a = PlayerAction()
        self.session.add(a)
        self.session.commit()
        c = GameCondition(
            playerActionId=a.id,
            locationId = self.location.id,
            npcId = self.db_object.id
            )
        self.session.add(c)
        self.session.commit()
        
        self.loc_dialogs_fill()


    def on_delete(self):
        # TODO пофиксить
        conditions = self.session.query(GameCondition).filter(
                GameCondition.locationId == self.location.id,
                GameCondition.npcId == self.db_object.id
        ).all()
        for condition in conditions:
            self.session.delete(condition)
            self.session.commit()

        self.deleted.emit()

