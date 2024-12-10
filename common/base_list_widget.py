from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from .autoresize import AutoResizingListWidget
from .icons import add_icon


class BaseListWidget(QWidget):
    list_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)

        self.first_line_layout = QHBoxLayout()
        self.base_layout.addLayout(self.first_line_layout)
        self.first_line_layout.addWidget(QLabel(f"{self.list_name()}:")) 
        self.fill_first_line()
        self.add_button = QPushButton()
        self.add_button.setIcon(add_icon())
        self.add_button.clicked.connect(self.on_add)
        self.first_line_layout.addWidget(self.add_button)

        self.fill_head()

        self.item_list = AutoResizingListWidget()
        self.base_layout.addWidget(self.item_list)
        self.fill_list()

    def list_name(self) -> str:
        return 'list'

    def fill_first_line(self):
        pass

    def fill_head(self):
        pass

    def query_list(self) -> list:
        return []

    def widget_of(self, db_object) -> QWidget:
        return QWidget()

    def add_default_element(self):
        pass

    def fill_list(self):
        self.item_list.clear()
        self.session = Session()

        for db_object in self.query_list():
            item = QListWidgetItem(self.item_list)
            widget = self.widget_of(db_object)
            widget.deleted.connect(self.fill_list)
            widget.changed.connect(self.list_changed)
            self.item_list.setItemWidget(item, widget)
            # item.setSizeHint(widget.sizeHint())

    def on_add(self):
        self.add_default_element()
        self.fill_list()
        self.list_changed.emit()