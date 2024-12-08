from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.location_npc_widget import LocationNpcWidget
from widgets.location_item_widget import LocationGameItemWidget
from common import BaseMapObject, AutoResizingListWidget
from .action_widget import ActionWidget


class LocationWidget(BaseMapObject):
    item_list_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        BaseMapObject.disconnect_all(self)
        self.row += 1
        self.base_layout.addWidget(QLabel("Description:"), self.row, 0, 1, 1)  # Метка для описания
        self.base_layout.addWidget(self.description, self.row, 1, 1, -1)  # Описание занимает всю оставшуюся ширину

        # Четвертая строка: список NPC (npc_list)
        self.row += 1
        tmp_layout = QHBoxLayout()
        self.base_layout.addLayout(tmp_layout, self.row, 0)
        tmp_layout.addWidget(QLabel("NPC List:")) 
        self.npc_combobox = QComboBox()
        if IS_EDITABLE:
            tmp_layout.addWidget(self.npc_combobox)
        self.appearance = QLineEdit()
        if IS_EDITABLE:
            tmp_layout.addWidget(self.appearance)
        self.add_npc_button = QPushButton()
        self.add_npc_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_npc_button.clicked.connect(self.on_add_npc)
        if IS_EDITABLE:
            tmp_layout.addWidget(self.add_npc_button)
        self.row += 1 # Метка для списка NPC
        self.npc_list = AutoResizingListWidget()
        self.base_layout.addWidget(self.npc_list, self.row, 0, 1, -1) 

        
        self.row += 1
        tmp_layout = QHBoxLayout()
        self.base_layout.addLayout(tmp_layout, self.row, 0)
        tmp_layout.addWidget(QLabel("Action List:"))
        tmp_layout.addStretch()

        self.add_action_button = QPushButton()
        self.add_action_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_action_button.clicked.connect(self.on_add_action)
        if IS_EDITABLE:
            tmp_layout.addWidget(self.add_action_button)
        self.row += 1 # Метка для списка NPC
        self.action_list = AutoResizingListWidget()
        self.base_layout.addWidget(self.action_list, self.row, 0, 1, -1) 
        self.row += 1 # Метка для списка NPC
        self.items_list = AutoResizingListWidget()
        self.base_layout.addWidget(self.items_list, self.row, 0, 1, -1) 

        self.connect_all()

    def on_location_selected(self, location_id: int) -> None:
        self.session = Session()
        self.object = self.session.query(Location).filter(Location.id == location_id).first()
        if self.object is None:
            return
        self.setup_map_object()

        self.disconnect_all()
        self.description.setHtml(self.object.description)
        self.connect_all()

        self.set_npcs()
        self.set_actions()
        self.set_items()

    def connect_all(self):
        super().connect_all()
        self.description.textChanged.connect(self.on_save)

    def disconnect_all(self):
        super().disconnect_all()
        self.description.textChanged.disconnect(self.on_save)

    def on_save(self):
        if self.object is None:
            return
        self.object.description = self.description.toHtml()
        super().on_save()

    def set_npcs(self):
        self.npc_combobox.clear()
        for npc in self.session.query(NPC).all():
            self.npc_combobox.addItem(npc.name, npc.id)

        self.npc_list.clear()

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
                widget = LocationNpcWidget(npc=npc, appearance=appearance[npc.id], location=self.object)
                widget.deleted.connect(self.set_npcs)
                self.npc_list.setItemWidget(item, widget)
                item.setSizeHint(widget.sizeHint())

    def on_add_npc(self):
        npc_id = self.npc_combobox.currentData()
        if self.session.query(NPC).filter(NPC.id == npc_id).first() is None:
            return
        # TODO Mark
        c = GameCondition(locationId=self.object.id, npcId=npc_id, text=self.appearance.text())
        self.session.add(c)
        self.session.commit()

        self.set_npcs()

    def set_items(self):
        self.items_list.clear()
        if self.object is None:
            return

        item_list = self.session.query(GameItem).join(WhereObject).filter(WhereObject.locationId == self.object.id).all()
        for game_item in item_list:
            item = QListWidgetItem(self.items_list)
            widget = LocationGameItemWidget(item=game_item)
            widget.deleted.connect(self.set_items)
            widget.item_moved.connect(self.item_list_changed)
            self.items_list.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

    def set_actions(self):
        self.action_list.clear()

        actions_conditions = check_marks_in_condition(
            self.session.query(GameCondition).filter(
                GameCondition.playerActionId != None,
                GameCondition.locationId == self.object.id,
                GameCondition.npcId == None
            ).all()
        )
        
        for condition in actions_conditions:
            action = self.session.query(PlayerAction).get(condition.playerActionId)
            if action is not None:
                item = QListWidgetItem(self.action_list)
                widget = ActionWidget(action_id=action.id)
                widget.deleted.connect(self.set_actions)
                self.action_list.setItemWidget(item, widget)
                item.setSizeHint(widget.sizeHint())


    def on_add_action(self):
        action = PlayerAction()
        self.session.add(action)
        self.session.commit()
        # TODO Mark
        c = GameCondition(locationId=self.object.id, playerActionId=action.id)
        self.session.add(c)
        self.session.commit()

        self.set_actions()


