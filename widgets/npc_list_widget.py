from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.location_npc_widget import LocationNpcWidget
from widgets.npc_widget import NpcWidget
from common import AutoResizingListWidget


class NpcListWidget(QWidget):
    npc_list_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)

        tmp_layout = QHBoxLayout()
        self.base_layout.addLayout(tmp_layout)
        tmp_layout.addWidget(QLabel("NPC List:")) 
        self.npc_name = QLineEdit()
        tmp_layout.addWidget(self.npc_name)
        self.add_npc_button = QPushButton()
        self.add_npc_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_npc_button.clicked.connect(self.on_add_npc)
        tmp_layout.addWidget(self.add_npc_button)

        self.npc_list = AutoResizingListWidget()
        self.base_layout.addWidget(self.npc_list)
        self.fill_npcs()

    def fill_npcs(self):
        self.npc_list.clear()
        self.session = Session()

        npc_list = self.session.query(NPC).all()
        for npc in npc_list:
            self.npc_list.addItem
            item = QListWidgetItem(self.npc_list)
            widget = NpcWidget(npc=npc)
            widget.deleted.connect(self.fill_npcs)
            self.npc_list.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

    def on_add_npc(self):
        npc = NPC(name=self.npc_name.text())
        self.session.add(npc)
        self.session.commit()
        self.fill_npcs()
        self.npc_list_changed.emit()