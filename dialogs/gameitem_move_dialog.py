from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QListWidget, QPushButton, QLineEdit, QLabel
)
from PyQt5.QtCore import Qt
from scheme import *

class GameItemMoveDialog(QDialog):
    def __init__(self, item: GameItem):
        super().__init__()
        self.item = item
        self.setWindowTitle(f"Move item '{self.item.name}'")
        self.session = Session()

        # Создаем таблицу
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Только одна колонка для отображения строки
        self.table.setHorizontalHeaderLabels(["Location", "Players", "NPC"])

        

        self.table.setRowCount(max([
            self.session.query(Location).count(),
            self.session.query(PlayerCharacter).count(),
            self.session.query(NPC).count(),
        ]))

        for row, location in enumerate(self.session.query(Location).all()):
            item = QTableWidgetItem(location.name)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setData(Qt.UserRole, location.id)
            self.table.setItem(row, 0, item)

        for row, player in enumerate(self.session.query(PlayerCharacter).all()):
            item = QTableWidgetItem(player.name)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setData(Qt.UserRole, player.id)
            self.table.setItem(row, 1, item)

        for row, npc in enumerate(self.session.query(NPC).all()):
            item = QTableWidgetItem(npc.name)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setData(Qt.UserRole, npc.id)
            self.table.setItem(row, 2, item)

        self.table.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

    def on_item_double_clicked(self, item: QTableWidgetItem):
        location_id, player_id, npc_id = None, None, None
        id_ = item.data(Qt.UserRole)
        if id_ is None:
            return
        if item.column() == 0:
            location_id = id_
        elif item.column() == 1:
            player_id = id_
        elif item.column() == 2:
            npc_id = id_
        else:
            return
        where = self.session.query(WhereObject).filter(WhereObject.gameItemId == self.item.id).first()
        if where is None:
            where = WhereObject(gameItemId=self.item.id)
            self.session.add(where)
        where.locationId = location_id
        where.playerId = player_id
        where.npcId = npc_id
        self.session.commit()

        self.accept()



