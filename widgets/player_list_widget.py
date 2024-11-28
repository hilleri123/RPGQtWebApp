from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.player_widget import PlayerWidget
from common import BaseMapObject, AutoResizingTextEdit, AutoResizingListWidget


class PlayerListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)

        tmp_layout = QHBoxLayout()
        self.base_layout.addLayout(tmp_layout)
        tmp_layout.addWidget(QLabel("Player List:")) 
        self.player_name = QLineEdit()
        tmp_layout.addWidget(self.player_name)
        self.add_player_button = QPushButton()
        self.add_player_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_player_button.clicked.connect(self.on_add_npc)
        tmp_layout.addWidget(self.add_player_button)

        self.player_list = AutoResizingListWidget()
        self.base_layout.addWidget(self.player_list)
        self.fill_players()

    def fill_players(self):
        self.player_list.clear()
        self.session = Session()

        for player in self.session.query(PlayerCharacter).all():
            # self.player_list.addItem
            item = QListWidgetItem(self.player_list)
            widget = PlayerWidget(player=player)
            self.player_list.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

    def on_add_npc(self):
        player = PlayerCharacter(name=self.player_name.text())
        self.session.add(player)
        self.session.commit()
        self.fill_players()
