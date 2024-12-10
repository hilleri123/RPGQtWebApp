from PyQt5.QtWidgets import QPushButton, QLabel, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from .files import open_img
from scheme import *
from repositories import *
from .html_text_edit_widget import HtmlTextEdit


class BaseMapObject(QWidget):
    map_object_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Session()
        self.name = QLineEdit()
        self.name.setReadOnly(not IS_EDITABLE)
        self.description = HtmlTextEdit()
        self.description.setReadOnly(not IS_EDITABLE)
        self.select_file_button = QPushButton("select file")
        self.select_file_button.clicked.connect(self.open_file_dialog)
        self.is_start_location = QCheckBox("Start")
        self.is_start_location.setEnabled(IS_EDITABLE)
        self.is_shown = QCheckBox("Show")
        self.coords = {"x": QSpinBox(), "y": QSpinBox(), "w": QSpinBox(), "h": QSpinBox()}
        
        self.object = None

        self.base_layout = QGridLayout(self)

        self.row = 0 
        self.base_layout.addWidget(QLabel("Name:"), self.row, 0)
        self.base_layout.addWidget(self.name, self.row, 1)
        self.base_layout.addWidget(self.select_file_button, self.row, 2)
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
        
        BaseMapObject.connect_all(self)


    def setup_map_object(self) -> None:
        if self.object is None:
            return
        self.disconnect_all()
        self.name.setText(self.object.name)
        tmp = self.object.is_shown if self.object.is_shown is not None else 2
        self.is_start_location.setChecked(tmp == 2) #
        self.is_shown.setChecked(tmp > 0) #

        self.coords["x"].setValue(self.object.offsetX if self.object.offsetX else 0)
        self.coords["y"].setValue(self.object.offsetY if self.object.offsetY else 0)
        self.coords["w"].setValue(self.object.width if self.object.width else 0)
        self.coords["h"].setValue(self.object.height if self.object.height else 0)

        self.connect_all()


    def on_save(self):
        if self.object is None:
            return
        self.object.name = self.name.text()
        self.object.offsetX = self.coords["x"].value()
        self.object.offsetY = self.coords["y"].value()
        self.object.width = self.coords["w"].value()
        self.object.height = self.coords["h"].value()
        if self.is_start_location.isChecked():
            self.object.is_shown = 2
        elif self.is_shown.isChecked():
            self.object.is_shown = 1
        else:
            self.object.is_shown = 0
        self.session.commit()
        self.map_object_updated.emit()

    def connect_all(self):
        self.name.textChanged.connect(self.on_save)
        self.is_start_location.stateChanged.connect(self.on_save)
        self.is_shown.stateChanged.connect(self.on_save)
        for _, w in self.coords.items():
            w.valueChanged.connect(self.on_save)

    def disconnect_all(self):
        self.name.textChanged.disconnect(self.on_save)
        self.is_start_location.stateChanged.disconnect(self.on_save)
        self.is_shown.stateChanged.disconnect(self.on_save)
        for _, w in self.coords.items():
            w.valueChanged.disconnect(self.on_save)
        

    def open_file_dialog(self):
        file_name = open_img(ICONS_DIR, self)
        if file_name:
            self.object.icon_file_path = file_name
            self.session.commit()
            self.map_object_updated.emit()
