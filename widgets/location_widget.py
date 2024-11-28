from PyQt5.QtWidgets import QPushButton, QLabel, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.npc_widget import NpcWidget
from common import BaseMapObject, AutoResizingTextEdit, AutoResizingListWidget


class LocationWidget(BaseMapObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.row += 1
        self.base_layout.addWidget(QLabel("Description:"), self.row, 0, 1, 1)  # Метка для описания
        self.base_layout.addWidget(self.description, self.row, 1, 1, -1)  # Описание занимает всю оставшуюся ширину

        # Четвертая строка: список NPC (npc_list)
        self.row += 1
        self.base_layout.addWidget(QLabel("NPC List:"), self.row, 0)  # Метка для списка NPC
        self.base_layout.addWidget(self.npc_list, self.row, 1, 1, -1) 

    def on_location_selected(self, location_id: int) -> None:
        self.session = Session()
        self.object = self.session.query(Location).filter(Location.id == location_id).first()
        if self.object is None:
            return

        self.setup_map_object()

        self.description.setText(self.object.description)
        
        self.set_npcs()


    def on_save(self):
        if self.object is None:
            return
        self.object.description = self.description.toHtml()

        super().on_save()

    def set_npcs(self):
        self.npc_list.clear()
        # for item in self.npc_list.children():
            # self.npc_list.removeItemWidget(item)
        # Получаем условия появления NPC
        npcs_conditions = check_marks_in_condition(
            self.session.query(GameCondition).filter(
                GameCondition.playerActionId == None,
                GameCondition.locationId == self.object.id,
                GameCondition.npcId != None
            ).all()
        )

        appearance = {}
        for npc_c in npcs_conditions:
            if npc_c.npcId in appearance:
                appearance[npc_c.npcId].append(npc_c.text)
            else:
                appearance[npc_c.npcId] = [npc_c.text]
        
        for npc_id in appearance:
            npc = self.session.query(NPC).filter(NPC.id == npc_id).first()
            if npc is not None:
                item = QListWidgetItem(self.npc_list)
                widget = NpcWidget(npc=npc, appearance=appearance[npc.id], location=self.object)
                self.npc_list.setItemWidget(item, widget)
                item.setSizeHint(widget.sizeHint())

