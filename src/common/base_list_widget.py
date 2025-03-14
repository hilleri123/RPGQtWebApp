from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from .autoresize import AutoResizingListWidget
from .icons import add_icon


class BaseListWidget(QWidget):
    list_changed = pyqtSignal()

    def __init__(self, auto_reload=False, parent=None):
        super().__init__(parent)
        self.auto_reload = auto_reload
        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)

        self.first_line_layout = QHBoxLayout()
        self.base_layout.addLayout(self.first_line_layout)
        self.first_line_layout.addWidget(QLabel(f"{self.list_name()}:")) 
        self.fill_first_line()
        self.show_hidden = QCheckBox()
        self.show_hidden.stateChanged.connect(self.fill_list)
        self.first_line_layout.addWidget(self.show_hidden)
        self.add_button = QPushButton()
        self.add_button.setIcon(add_icon())
        self.add_button.clicked.connect(self.on_add)
        self.first_line_layout.addWidget(self.add_button)

        self.fill_head()

        self.item_list = AutoResizingListWidget()
        self.item_list.setVerticalScrollMode(self.item_list.ScrollPerPixel)
        self.item_list.verticalScrollBar().setSingleStep(15)
        self.base_layout.addWidget(self.item_list)
        self.fill_list()

        self.on_editable_changed(changed_manager.everything_editalbe())
        changed_manager.editable_changed.connect(self.on_editable_changed)

    def on_editable_changed(self, is_editable):
        if is_editable:
            self.add_button.show()
        else:
            self.add_button.hide()

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
        scroll_position = self.item_list.verticalScrollBar().value()
        self.item_list.clear()
        self.session = Session()

        for db_object in self.query_list():
            item = QListWidgetItem(self.item_list)
            widget = self.widget_of(db_object)
            if self.show_hidden.isChecked() and widget.is_hidden():
                continue
            widget.deleted.connect(self.fill_list)
            if self.auto_reload:
                widget.changed.connect(self.fill_list)
            widget.changed.connect(self.list_changed)
            self.item_list.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())
        
        self.item_list.verticalScrollBar().setValue(scroll_position)

    def on_add(self):
        self.add_default_element()
        self.fill_list()
        self.list_changed.emit()
        self.item_list.setFocus()


