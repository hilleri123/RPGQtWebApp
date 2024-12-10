import os
import shutil
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QLineEdit, QDateTimeEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QLabel, QWidget, QListWidget
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QPolygonF
from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QPointF, QSize, Qt
import typing
from scheme import *
from .datetime_editor import DateTimeEditWidget
from .base_map_label import BaseMapLabel
from dialogs.polygon_dialog import PolygonDialog
from common import icons

class BaseMapWidget(QWidget):
    map_image_saved = pyqtSignal()
    map_changed = pyqtSignal(int)
    datetime_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        base_layout = QVBoxLayout()
        self.setLayout(base_layout)
        self.mapLabel = None
        self.setup_label()
        self.mapLabel.map_image_saved.connect(self.map_image_saved)
        base_layout.addWidget(self.mapLabel)
        self.button_layout = QHBoxLayout()
        base_layout.addLayout(self.button_layout)
        self.select_file_button = QPushButton("select file")
        self.select_file_button.clicked.connect(self.open_file_dialog)
        self.button_layout.addWidget(self.select_file_button)
        self.edit_polygon = QPushButton()
        self.edit_polygon.setIcon(icons.move_icon())
        self.edit_polygon.clicked.connect(self.show_point_dialog)
        self.button_layout.addWidget(self.edit_polygon)
        self.name_edit = QLineEdit("Name")
        if IS_EDITABLE:
            self.button_layout.addWidget(self.name_edit)
        self.add_item_button = QPushButton("add item")
        self.add_item_button.clicked.connect(self.add_item)
        if IS_EDITABLE:
            self.button_layout.addWidget(self.add_item_button)
        self.datetime_base_edit = QDateTimeEdit()
        self.datetime_base_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.datetime_base_edit.dateTimeChanged.connect(self.on_base_timeeditor)
        if IS_EDITABLE:
            self.button_layout.addWidget(self.datetime_base_edit)
        self.datetime_edit = DateTimeEditWidget()
        self.datetime_edit.dateTimeChanged.connect(self.on_timeeditor)
        self.button_layout.addWidget(self.datetime_edit)

        self.polygon_dialog = PolygonDialog()

        self.polygon_dialog.polygon_selected.connect(self.set_polygon_id)
        self.polygon_dialog.polygon_changed.connect(self.mapLabel.repaint)

        self.on_datetime_changed()
        self.datetime_changed.connect(self.on_datetime_changed)

    def setup_label(self):
        self.mapLabel = BaseMapLabel()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        # Открываем диалог выбора файла
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp);;Все файлы (*)",
            options=options
        )
        if file_name:
            self.mapLabel.set_file_path(file_name)

    def add_item(self):
        self.mapLabel.add_item(self.name_edit.text())

    def set_current_map(self, map_id: int):
        self.session = Session()
        record_to_update = self.session.query(SceneMap) \
            .filter(SceneMap.isCurrent == True).first()
        if record_to_update is not None:
            record_to_update.isCurrent = False
        # print(record_to_update.name, record_to_update.isCurrent)
        record_to_update = self.session.query(SceneMap) \
            .filter(SceneMap.id == map_id).first()
        if record_to_update is not None:
            record_to_update.isCurrent = True
        # print(record_to_update.name, record_to_update.isCurrent)
        self.session.commit()
        self.mapLabel.set_map()
        self.map_changed.emit(map_id)

    
    def on_map_update(self):
        self.mapLabel.set_map()

    def on_datetime_changed(self):
        self.session = Session()
        g_map = self.session.query(GlobalMap).first()
        if g_map is None:
            return
        dt = g_map.time
        if dt is not None:
            self.datetime_edit.setDateTime(dt)
            self.datetime_base_edit.setDateTime(dt)
    
    def on_base_timeeditor(self):
        self.set_time(self.datetime_base_edit.dateTime().toPyDateTime())

    def on_timeeditor(self):
        self.set_time(self.datetime_edit.dateTime().toPyDateTime())

    def set_time(self, dt):
        self.session = Session()
        g_map = self.session.query(GlobalMap).first()
        if g_map is None:
            return
        g_map.time = dt
        self.session.commit()
        for character in self.session.query(PlayerCharacter).all():
            if character.time is None or character.time < dt:
                character.time = dt
                self.session.commit()
        
        self.datetime_changed.emit()


    def show_point_dialog(self):
        self.polygon_dialog.show()

    def set_polygon_id(self, polygon_id):
        self.mapLabel.set_polygon_id(polygon_id)
