from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *
from common import AutoResizingTextEdit, AutoResizingListWidget
from .npc_widget import NpcWidget


class LocationNpcWidget(NpcWidget):
    def __init__(self, npc: NPC, appearance: list[str] = None, location: Location = None, parent=None):
        super().__init__(npc, parent, appearance=appearance, location=location)

    def setup(self, appearance, location):
        super().setup()
        self.location = location
        loc_dialogs = []
        if location is not None:
            loc_dialogs = check_marks_in_condition(
                self.session.query(GameCondition).filter(
                    GameCondition.playerActionId != None,
                    GameCondition.locationId == location.id,
                    GameCondition.npcId == self.npc.id
                ).all()
            )

        # TODO редактировать appearance
        if appearance is not None:
            self.appearance_field = AutoResizingTextEdit()  # Поле для списка внешностей (appearance)
            self.appearance_field.setText('; '.join(appearance))
            self.appearance_field.setReadOnly(True)
            self.base_layout.addWidget(self.appearance_field)

        self.loc_dialogs_list = AutoResizingListWidget()  # Список локальных диалогов
        
        self.base_layout.addWidget(QLabel("Локальные диалоги:"))
        self.base_layout.addWidget(self.loc_dialogs_list)


    def on_edit_npc(self):
        pass #TODO


    def on_add_dialog(self):
        pass #TODO


    def on_delete(self):
        pass #TODO

