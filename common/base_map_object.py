from PyQt5.QtWidgets import QPushButton, QLabel, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *
from widgets.npc_widget import NpcWidget
from common import AutoResizingTextEdit, AutoResizingListWidget


class BaseMapObject(QWidget):
    map_object_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Session()
        self.name = QLineEdit()
        self.name.setReadOnly(not IS_EDITABLE)
        self.description = AutoResizingTextEdit()
        self.description.setReadOnly(not IS_EDITABLE)
        self.save = QPushButton()
        self.save.setEnabled(IS_EDITABLE)
        self.save.setIcon(QIcon.fromTheme("document-save"))
        self.save.clicked.connect(self.on_save)
        self.is_start_location = QCheckBox("Start")
        self.is_start_location.setEnabled(IS_EDITABLE)
        self.is_shown = QCheckBox("Show")
        self.coords = {"x": QSpinBox(), "y": QSpinBox(), "w": QSpinBox(), "h": QSpinBox()}
        self.npc_list = AutoResizingListWidget()
        self.object = None

        self.base_layout = QGridLayout(self)

        self.row = 0 
        self.base_layout.addWidget(QLabel("Name:"), self.row, 0)
        self.base_layout.addWidget(self.name, self.row, 1)
        self.base_layout.addWidget(self.save, self.row, 2)
        if self.is_start_location is not None:
            self.base_layout.addWidget(self.is_start_location, self.row, 3)
        self.base_layout.addWidget(self.is_shown, self.row, 4)

        if IS_EDITABLE:
            self.row += 1
            col = 0
            for key, val in self.coords.items():
                self.base_layout.addWidget(QLabel(key), self.row, col)  # Метка координаты
                col += 1
                val.setMinimum(0)
                val.setMaximum(10000)
                self.base_layout.addWidget(val, self.row, col)  # Поле ввода координаты
                col += 1


    def setup_map_object(self) -> None:
        if self.object is None:
            return
        self.name.setText(self.object.name)
        tmp = self.object.is_shown if self.object.is_shown is not None else 2
        self.is_start_location.setChecked(tmp == 2) #
        self.is_shown.setChecked(tmp > 0) #
        self.coords["x"].setValue(self.object.offsetX)
        self.coords["y"].setValue(self.object.offsetY)
        self.coords["w"].setValue(self.object.width)
        self.coords["h"].setValue(self.object.height)


    def on_save(self):
        if self.object is None:
            return
        self.object.name = self.name.text()
        self.object.offsetX = self.coords["x"].value()
        self.object.offsetY = self.coords["y"].value()
        self.object.width = self.coords["h"].value()
        self.object.height = self.coords["w"].value()
        if self.is_start_location.isChecked():
            self.object.is_shown = 2
        elif self.is_shown.isChecked():
            self.object.is_shown = 1
        else:
            self.object.is_shown = 0
        self.session.commit()
        self.map_object_updated.emit()

