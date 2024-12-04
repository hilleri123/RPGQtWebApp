from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.location_npc_widget import LocationNpcWidget
from widgets.note_widget import NoteWidget
from common import BaseMapObject, AutoResizingTextEdit, AutoResizingListWidget


class NoteListWidget(QWidget):
    noteschange = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)

        tmp_layout = QHBoxLayout()
        self.base_layout.addLayout(tmp_layout)
        tmp_layout.addWidget(QLabel("Note List:")) 
        self.add_note_button = QPushButton()
        self.add_note_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_note_button.clicked.connect(self.on_add_note)
        tmp_layout.addWidget(self.add_note_button)

        self.note_list = AutoResizingListWidget()
        self.base_layout.addWidget(self.note_list)
        self.fill_notes()

    def fill_notes(self):
        self.note_list.clear()
        self.session = Session()

        note_list = self.session.query(Note).all()
        for note in note_list:
            self.note_list.addItem
            item = QListWidgetItem(self.note_list)
            widget = NoteWidget(note=note)
            widget.deleted.connect(self.fill_notes)
            self.note_list.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

    def on_add_note(self):
        npc = Note()
        self.session.add(npc)
        self.session.commit()
        self.fill_notes()
        self.noteschange.emit()