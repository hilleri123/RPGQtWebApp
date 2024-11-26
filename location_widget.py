from PyQt5.QtWidgets import QPushButton, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel


class LocationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Session()
        self.name = QLineEdit()
        self.name.setReadOnly(not IS_EDITABLE)
        self.description = QTextEdit()
        self.description.setReadOnly(not IS_EDITABLE)
        self.save = QPushButton()
        self.save.setEnabled(IS_EDITABLE)
        self.save.clicked.connect(self.on_save)
        self.location = None
        self.npc_model = NpcTreeModel(self.location)
        tree_view = QTreeView()
        tree_view.setModel(self.npc_model)
        layout = QVBoxLayout(self)
        tmp_layout = QHBoxLayout()
        layout.addLayout(tmp_layout)
        tmp_layout.addWidget(self.name)
        tmp_layout.addWidget(self.save)
        layout.addWidget(self.description)
        layout.addWidget(tree_view)

    def on_location_selected(self, location_id: int) -> None:
        self.location = self.session.query(Location).filter(Location.id == location_id).first()
        if self.location is None:
            return

        self.npc_model.set_location(self.location)
        self.name.setText(self.location.name)
        self.description.setText(self.location.description)

    def on_save(self):
        if self.location is None:
            return
        self.location.name = self.name.text()
        self.location.description = self.description.toHtml()
        self.session.commit()