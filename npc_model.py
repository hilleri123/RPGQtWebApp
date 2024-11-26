from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QVariant, Qt
from scheme import *
from dataclasses import dataclass
from repositories import *


class Holder:
    def __init__(self):
        self.parent = None

    def children(self):
        return []

    def data(self, clm):
        return None

    def column(self):
        return 0


@dataclass()
class PlayerActionHolder(Holder):
    parent: Holder
    action: PlayerAction

    def data(self, clm):
        return self.action.id

    def column(self):
        return 1


@dataclass()
class NpcHolder(Holder):
    npc: NPC
    appearance: list[str]
    loc_dialogs: list[PlayerActionHolder]
    dialogs: list[PlayerActionHolder]

    def children(self):
        return self.loc_dialogs + self.dialogs

    def data(self, clm):
        if clm == 0 and self.npc is not None:
            return self.npc.name
        elif clm == 1:
            return '\n'.join(self.appearance)
        return None

    def column(self):
        return 2


class NpcTreeModel(QAbstractItemModel):
    def __init__(self, location: Location, parent=None):
        super().__init__(parent)
        self.session = Session()
        self.npcs = []
        self.set_location(location)

    def set_location(self, location: Location):
        self.beginResetModel()
        self.npcs = []
        if location is None:
            return
        npcs_conditions = check_marks_in_condition(self.session.query(GameCondition).filter(
            GameCondition.playerActionId == None,
            GameCondition.locationId == location.id,
            GameCondition.npcId != None
        ).all())  # appearence
        appearance = {}
        for npc_c in npcs_conditions:
            if npc_c.npcId in appearance:
                appearance[npc_c.npcId].append(npc_c.text)
            else:
                appearance[npc_c.npcId] = [npc_c.text]
        for npc_id in appearance:
            npc = self.session.query(NPC).filter(NPC.id == npc_id).first()
            loc_dialogs = check_marks_in_condition(self.session.query(GameCondition).filter(
                GameCondition.playerActionId != None,
                GameCondition.locationId == location.id,
                GameCondition.npcId == npc_id
            ).all())
            dialogs = check_marks_in_condition(self.session.query(GameCondition).filter(
                GameCondition.playerActionId != None,
                GameCondition.locationId == None,
                GameCondition.npcId == npc_id
            ).all())
            self.npcs.append(NpcHolder(
                npc=npc,
                appearance=appearance[npc_id],
                loc_dialogs=[PlayerActionHolder(parent=len(self.npcs), action=i) for i in loc_dialogs],
                dialogs=[PlayerActionHolder(parent=len(self.npcs), action=i) for i in dialogs]
            ))
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            return len(self.npcs)
        if type(parent.internalPointer()) is PlayerActionHolder:
            return 0
        if type(parent.internalPointer()) is NpcHolder:
            npc_holder = parent.internalPointer()
            return len(npc_holder.children())
        return 0

    def columnCount(self, paren: QModelIndex = ...):
        return 2

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        item = index.internalPointer()
        if role == Qt.DisplayRole:
            return item.data(index.column())

        return QVariant()

    def headerData(self, column, orientation, role):
        if (orientation == Qt.Horizontal and role == Qt.DisplayRole):
            return QVariant("Npcs")

        return QVariant()

    def index(self, row, column, parent):
        if not parent.isValid(): #!!!!!!!!!!
            return self.createIndex(row, column, self.npcs[row])

        if type(parent.internalPointer()) is PlayerActionHolder:
            return QModelIndex()

        if type(parent.internalPointer()) is NpcHolder:
            npc_holder = parent.internalPointer()
            return self.createIndex(row, column, npc_holder.children()[row])

        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        item = index.internalPointer()
        if not item or type(item) is NpcHolder:
            return QModelIndex()

        return self.createIndex(item.parent, 0, QModelIndex())
