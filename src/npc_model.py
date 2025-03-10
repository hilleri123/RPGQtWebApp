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


@dataclass
class PlayerActionHolder(Holder):
    parent: Holder
    action: PlayerAction

    def data(self, clm):
        if clm == 0:
            return self.action.id
        return None

    def column(self):
        return 1


@dataclass
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
            self.endResetModel()  # Завершаем сброс модели, если локация пустая
            return

        # Получаем условия появления NPC
        npcs_conditions = check_marks_in_condition(
            self.session.query(GameCondition).filter(
                GameCondition.playerActionId == None,
                GameCondition.locationId == location.id,
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
            
            loc_dialogs = check_marks_in_condition(
                self.session.query(GameCondition).filter(
                    GameCondition.playerActionId != None,
                    GameCondition.locationId == location.id,
                    GameCondition.npcId == npc_id
                ).all()
            )
            
            dialogs = check_marks_in_condition(
                self.session.query(GameCondition).filter(
                    GameCondition.playerActionId != None,
                    GameCondition.locationId == None,
                    GameCondition.npcId == npc_id
                ).all()
            )
            
            # Создаем NpcHolder с корректным parent для дочерних элементов
            npc_holder = NpcHolder(
                npc=npc,
                appearance=appearance[npc_id],
                loc_dialogs=[
                    PlayerActionHolder(parent=None, action=i) for i in loc_dialogs
                ],
                dialogs=[
                    PlayerActionHolder(parent=None, action=i) for i in dialogs
                ]
            )
            
            # Устанавливаем parent для дочерних элементов
            for child in npc_holder.children():
                child.parent = npc_holder
            
            self.npcs.append(npc_holder)
        
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            return len(self.npcs)

        item = parent.internalPointer()
        
        if isinstance(item, PlayerActionHolder):
            return 0
        
        if isinstance(item, NpcHolder):
            return len(item.children())
        
        return 0

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 2

    def data(self, index: QModelIndex, role: int) -> QVariant:
        if not index.isValid():
            return QVariant()

        item = index.internalPointer()
        
        if role == Qt.DisplayRole and item is not None:
            return item.data(index.column())
        
        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int) -> QVariant:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "NPC Name"
            elif section == 1:
                return "Appearance"
        
        return QVariant()

    def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
        if not parent.isValid():
            if row < len(self.npcs):
                return self.createIndex(row, column, self.npcs[row])

        item = parent.internalPointer()
        
        if isinstance(item, NpcHolder) and row < len(item.children()):
            child_item = item.children()[row]
            return self.createIndex(row, column, child_item)

        return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        item = index.internalPointer()
        
        if isinstance(item, PlayerActionHolder) and item.parent is not None:
            parent_item = item.parent
            row = self.npcs.index(parent_item)
            return self.createIndex(row, 0, parent_item)

        if isinstance(item, NpcHolder):
            return QModelIndex()

        return QModelIndex()
    
    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        
        item = index.internalPointer()
        
        # Проверяем тип элемента и разрешаем редактирование
        if isinstance(item, PlayerActionHolder):
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled