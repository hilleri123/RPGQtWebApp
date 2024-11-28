import os
import shutil
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QLineEdit, QDateTimeEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QLabel, QWidget, QListWidget
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent
from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QSize, Qt
import typing
from scheme import SceneMap, GlobalMap, PlayerCharacter, Session, IS_EDITABLE
from .datetime_editor import DateTimeEditWidget



class BaseMapLabel(QLabel):
    item_clicked = pyqtSignal(int)
    time_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.original = QPixmap()
        self.map = None
        self.items = []

    def mousePressEvent(self, ev: typing.Optional[QMouseEvent]) -> None:
        if ev is None:
            return
        pos = ev.pos()

        for item in self.items:
            if self.item_rect(item).contains(pos):
                if ev.button() == Qt.RightButton:
                    self.show_context_menu(ev.globalPos(), item)
                else:
                    self.item_clicked.emit(item.id)
                break

    def paintEvent(self, a0: typing.Optional[QPaintEvent]) -> None:
        super().paintEvent(a0)
        painter = QPainter(self)

        for item in self.items:
            if item.is_shown == 2:
                painter.setPen(QColor(0, 0, 255))
            elif item.is_shown > 0:
                painter.setPen(QColor(0, 255, 0))
            else:
                painter.setPen(QColor(255, 0, 0))
            painter.drawRect(self.item_rect(item))

    def item_rect(self, item) -> QRect:
        if item is None or self.original.width() == 0 or self.original.height() == 0:
            return QRect()
        w_aspect = self.size().width() / self.original.width()
        h_aspect = self.size().height() / self.original.height()
        return QRect(QPoint(int(item.offsetX * w_aspect),
                     int(item.offsetY * h_aspect)),
                     QSize(int(item.width * w_aspect),
                     int(item.height * h_aspect)))

    def set_file_path(self, file_path):
        if self.map is not None and self.session is not None:
            file_name = os.path.basename(file_path)
            destination_directory = 'data/imgs'
            if os.path.isfile(os.path.join(destination_directory, file_name)):
                print(f"Warning: Файл с именем '{file_name}' уже существует в директории '{destination_directory}'.")

            destination_path = os.path.join(destination_directory, file_name)
            shutil.copy2(file_path, destination_path)

            self.map.filePath = file_name
            self.session.commit()
            self.set_map()

    def show_context_menu(self, pos, item):
        self.session = Session()
        menu = QMenu(self)
        action_show = QAction("Toggle", self)
        action_show.triggered.connect(lambda: self.toggle_item_visibility(item))
        menu.addAction(action_show)

        for character in self.session.query(PlayerCharacter).all():
            action = QAction(character.name, self)
            action.setCheckable(True)
            action.setChecked(self.character_presence(item, character))
            action.triggered.connect(lambda checked, c=character: self.toggle_character_presence(item, c))
            menu.addAction(action)
        menu.exec_(pos)


    def character_presence(self, item, character):
        pass

    def toggle_character_presence(self, item, character):
        pass
        # character.
        # self.session.commit()

    def toggle_item_visibility(self, item):
        if item.is_shown != 2:
            if item.is_shown > 0:
                item.is_shown = 0
            else:
                item.is_shown = 1
            self.session.commit()
            self.repaint()

    def add_item(self, name):
        pass

    def set_map(self):
        pass


class BaseMapWidget(QWidget):
    map_changed = pyqtSignal(int)
    datetime_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        base_layout = QVBoxLayout()
        self.setLayout(base_layout)
        self.mapLabel = None
        self.setup_label()
        base_layout.addWidget(self.mapLabel)
        self.button_layout = QHBoxLayout()
        base_layout.addLayout(self.button_layout)
        self.select_file_button = QPushButton("select file")
        self.select_file_button.clicked.connect(self.open_file_dialog)
        self.button_layout.addWidget(self.select_file_button)
        self.name_edit = QLineEdit("Name")
        if IS_EDITABLE:
            self.button_layout.addWidget(self.name_edit)
        self.add_item_button = QPushButton("add item")
        self.add_item_button.clicked.connect(self.add_item)
        if IS_EDITABLE:
            self.button_layout.addWidget(self.add_item_button)
        self.datetime_base_edit = QDateTimeEdit()
        self.datetime_base_edit.dateTimeChanged.connect(self.on_base_timeeditor)
        if IS_EDITABLE:
            self.button_layout.addWidget(self.datetime_base_edit)
        self.datetime_edit = DateTimeEditWidget()
        self.datetime_edit.dateTimeChanged.connect(self.on_timeeditor)
        self.button_layout.addWidget(self.datetime_edit)

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
        g_map = self.session.query(GlobalMap).first()
        if g_map is None:
            return
        dt = g_map.time
        self.datetime_edit.setDateTime(dt)
        self.datetime_base_edit.setDateTime(dt)
    
    def on_base_timeeditor(self):
        self.session = Session()
        g_map = self.session.query(GlobalMap).first()
        if g_map is None:
            return
        dt = self.datetime_base_edit.dateTime().toPyDateTime()
        g_map.time = dt
        self.session.commit()
        for character in self.session.query(PlayerCharacter).all():
            character.time = dt
            self.session.commit()
        
        self.datetime_changed.emit()

    def on_timeeditor(self):
        g_map = self.session.query(GlobalMap).first()
        if g_map is None:
            return
        g_map.time = self.datetime_edit.dateTime().toPyDateTime()
        self.session.commit()
        
        self.datetime_changed.emit()
