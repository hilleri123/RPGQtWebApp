from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidgetItem, QFormLayout, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *
from common import AutoResizingTextEdit, BaseListWidget, AutoResizingListWidget
from .npc_widget import NpcWidget
from .action_widget import ActionWidget



class LocationNpcDialogList(BaseListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def list_name(self):
        return 'Локальные диалоги:'

    def set_npc_location_id(self, npc_id, location_id):
        self.npc_id = npc_id
        self.location_id = location_id
        self.fill_list()

    def query_list(self) -> list:
        try:
            if self.npc_id is None or self.location_id is None:
                return []
        except AttributeError:
            return []
        
        return self.session.query(PlayerAction).join(GameCondition).filter(
                GameCondition.playerActionId != None,
                GameCondition.locationId == self.location_id,
                GameCondition.npcId == self.npc_id
            ).all()

    def widget_of(self, db_object) -> QWidget:
        return ActionWidget(db_object)
    
    def add_default_element(self):
        action = PlayerAction()
        self.session.add(action)
        self.session.commit()
        # TODO Mark
        c = GameCondition(npcId=self.npc_id, locationId=self.location_id, playerActionId=action.id)
        self.session.add(c)
        self.session.commit()

class LocationNpcWidget(NpcWidget):
    def __init__(self, npc: NPC, appearance: list[str] = None, location: Location = None, parent=None):
        super().__init__(npc, parent, appearance=appearance, location=location)
        self.on_edit_npc()

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

        self.loc_dialogs_list = LocationNpcDialogList()  # Список локальных диалогов
        self.loc_dialogs_list.set_npc_location_id(self.db_object.id, location.id)
        self.base_layout.addWidget(self.loc_dialogs_list)

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
        self.setMinimumWidth(self.width())
        self.adjustSize()
        self.setMinimumWidth(10)

        self.set_hint.emit(self.sizeHint())
        # if self.parent():
        #     w0 = self.parent()
        #     w0.setSizeHint()
        #     if w0:
        #         list_w = w0.parent()
        #         if list_w and issubclass(AutoResizingListWidget, type(list_w)):
        #             list_w.auto_resize()
                    # print('!')
            # self.parent.auto_resize()
        #TODO minimaze


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

