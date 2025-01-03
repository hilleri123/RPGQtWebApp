from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.location_npc_widget import LocationNpcWidget
from widgets.location_item_widget import LocationGameItemWidget
from common import BaseMapObject, AutoResizingListWidget, BaseListWidget, icons
from .action_widget import ActionWidget
from .item_list_widget import ItemListWidget
from .npc_list_widget import NpcListWidget


class LocationItemListWidget(ItemListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.add_button.setEnabled(False)

    def fill_first_line(self):
        pass

    def fill_head(self):
        pass

    def set_location(self, location_id):
        self.location_id = location_id
        self.fill_list()

    def query_list(self) -> list:
        try:
            if self.location_id is None:
                return []
        except AttributeError:
            return []
        return self.session.query(GameItem).join(WhereObject).filter(WhereObject.locationId == self.location_id).all()
    
    def widget_of(self, db_object) -> QWidget:
        return LocationGameItemWidget(db_object)
    
    def add_default_element(self):
        pass


class LocationNPCListWidget(NpcListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.location_id = None

    def fill_first_line(self):
        self.npc_combobox = QComboBox()
        if IS_EDITABLE:
            self.first_line_layout.addWidget(self.npc_combobox)
        self.appearance = QLineEdit()
        if IS_EDITABLE:
            self.first_line_layout.addWidget(self.appearance)

    def fill_head(self):
        pass

    def set_location(self, location_id):
        self.location_id = location_id
        self.fill_list()

    def query_list(self) -> list:
        try:
            if self.location_id is None:
                return []
        except AttributeError:
            return []
        self.npc_combobox.clear()
        for npc in self.session.query(NPC).all():
            self.npc_combobox.addItem(npc.name, npc.id)
        
        npcs_conditions = check_marks_in_condition(
            self.session.query(GameCondition).filter(
                GameCondition.playerActionId == None,
                GameCondition.locationId == self.location_id,
                GameCondition.npcId != None
            ).all()
        )

        appearance = {}
        for npc_c in npcs_conditions:
            if npc_c.npcId in appearance:
                appearance[npc_c.npcId].append(npc_c.text)
            else:
                appearance[npc_c.npcId] = [npc_c.text]
        
        res = []
        for npc_id in appearance:
            npc = self.session.query(NPC).filter(NPC.id == npc_id).first()
            if npc is not None:
                res.append({"npc":npc, "appearance":appearance[npc.id]})
        res = sorted(res, key=lambda x: x["npc"].isDead)
        return res
    
    def widget_of(self, item) -> QWidget:
        location = self.session.query(Location).filter(Location.id == self.location_id).first()
        if location is None:
            return
        return LocationNpcWidget(npc=item["npc"], appearance=item["appearance"], location=location)
    
    def add_default_element(self):
        if self.location_id is None:
            return
        npc_id = self.npc_combobox.currentData()
        if self.session.query(NPC).filter(NPC.id == npc_id).first() is None:
            return
        # TODO Mark
        c = GameCondition(locationId=self.location_id, npcId=npc_id, text=self.appearance.text())
        self.session.add(c)
        self.session.commit()


class LocationActionList(BaseListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_location(self, location_id):
        self.location_id = location_id
        self.fill_list()

    def query_list(self) -> list:
        try:
            if self.location_id is None:
                return []
        except AttributeError:
            return []
        
        return self.session.query(PlayerAction).join(GameCondition).filter(
                GameCondition.playerActionId != None,
                GameCondition.locationId == self.location_id,
                GameCondition.npcId == None
            ).all()

    def widget_of(self, db_object) -> QWidget:
        return ActionWidget(db_object)
    
    def add_default_element(self):
        action = PlayerAction()
        self.session.add(action)
        self.session.commit()
        # TODO Mark
        c = GameCondition(locationId=self.location_id, playerActionId=action.id)
        self.session.add(c)
        self.session.commit()

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
        self.npc_list = LocationNPCListWidget()
        self.base_layout.addWidget(self.npc_list, self.row, 0, 1, -1) 

        
        self.row += 1
        tmp_layout = QHBoxLayout()
        self.base_layout.addLayout(tmp_layout, self.row, 0)
        tmp_layout.addWidget(QLabel("Action List:"))
        tmp_layout.addStretch()

        self.row += 1 # Метка для списка NPC
        self.action_list = LocationActionList()
        self.base_layout.addWidget(self.action_list, self.row, 0, 1, -1) 
        self.row += 1 # Метка для списка NPC
        self.items_list = LocationItemListWidget()
        self.items_list.list_changed.connect(self.item_list_changed)
        self.base_layout.addWidget(self.items_list, self.row, 0, 1, -1) 

        self.connect_all()

    def on_location_selected(self, location_id: int) -> None:
        self.session = Session()
        self.object = self.session.query(Location).filter(Location.id == location_id).first()
        if self.object is None:
            return
        self.setup_map_object()

        self.disconnect_all()
        self.description.clear()
        self.description.setHtml(self.object.description)
        self.connect_all()

        self.npc_list.set_location(location_id)
        self.items_list.set_location(location_id)
        self.action_list.set_location(location_id)

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

    # def set_npcs(self):
        # self.npc_combobox.clear()
        # for npc in self.session.query(NPC).all():
        #     self.npc_combobox.addItem(npc.name, npc.id)

    #     self.npc_list.clear()

    #     npcs_conditions = check_marks_in_condition(
    #         self.session.query(GameCondition).filter(
    #             GameCondition.playerActionId == None,
    #             GameCondition.locationId == self.object.id,
    #             GameCondition.npcId != None
    #         ).all()
    #     )

    #     appearance = {}
    #     for npc_c in npcs_conditions:
    #         if npc_c.npcId in appearance:
    #             appearance[npc_c.npcId].append(npc_c.text)
    #         else:
    #             appearance[npc_c.npcId] = [npc_c.text]
        
    #     for npc_id in appearance:
    #         npc = self.session.query(NPC).filter(NPC.id == npc_id).first()
    #         if npc is not None:
    #             item = QListWidgetItem(self.npc_list)
    #             widget = LocationNpcWidget(npc=npc, appearance=appearance[npc.id], location=self.object)
    #             widget.deleted.connect(self.set_npcs)
    #             self.npc_list.setItemWidget(item, widget)
    #             item.setSizeHint(widget.sizeHint())

    # def on_add_npc(self):
    #     npc_id = self.npc_combobox.currentData()
    #     if self.session.query(NPC).filter(NPC.id == npc_id).first() is None:
    #         return
    #     # TODO Mark
    #     c = GameCondition(locationId=self.object.id, npcId=npc_id, text=self.appearance.text())
    #     self.session.add(c)
    #     self.session.commit()

    #     self.set_npcs()

    # def set_items(self):
    #     self.items_list.clear()
    #     if self.object is None:
    #         return

    #     item_list = self.session.query(GameItem).join(WhereObject).filter(WhereObject.locationId == self.object.id).all()
    #     for game_item in item_list:
    #         item = QListWidgetItem(self.items_list)
    #         widget = LocationGameItemWidget(item=game_item)
    #         widget.deleted.connect(self.set_items)
    #         widget.item_moved.connect(self.item_list_changed)
    #         self.items_list.setItemWidget(item, widget)
    #         item.setSizeHint(widget.sizeHint())

    # def set_actions(self):
    #     self.action_list.clear()

    #     actions_conditions = check_marks_in_condition(
    #         self.session.query(GameCondition).filter(
    #             GameCondition.playerActionId != None,
    #             GameCondition.locationId == self.object.id,
    #             GameCondition.npcId == None
    #         ).all()
    #     )
        
    #     for condition in actions_conditions:
    #         action = self.session.query(PlayerAction).get(condition.playerActionId)
    #         if action is not None:
    #             item = QListWidgetItem(self.action_list)
    #             widget = ActionWidget(action_id=action.id)
    #             widget.deleted.connect(self.set_actions)
    #             self.action_list.setItemWidget(item, widget)
    #             item.setSizeHint(widget.sizeHint())


    # def on_add_action(self):
    #     action = PlayerAction()
    #     self.session.add(action)
    #     self.session.commit()
    #     # TODO Mark
    #     c = GameCondition(locationId=self.object.id, playerActionId=action.id)
    #     self.session.add(c)
    #     self.session.commit()

    #     self.set_actions()


