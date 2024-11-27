from PyQt5.QtWidgets import QPushButton, QLabel, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from npc_model import NpcTreeModel
from repositories import *
from widgets.npc_widget import NpcWidget
from common import AutoResizingTextEdit, AutoResizingListWidget


class LocationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.session = Session()
        self.name = QLineEdit()
        self.name.setReadOnly(not IS_EDITABLE)
        self.description = AutoResizingTextEdit()
        self.description.setReadOnly(not IS_EDITABLE)
        self.save = QPushButton()
        self.save.setIcon(QIcon.fromTheme("document-save"))
        self.save.setEnabled(IS_EDITABLE)
        self.save.clicked.connect(self.on_save)
        self.is_start_location = QCheckBox("Start") if IS_EDITABLE else None
        self.is_shown = QCheckBox("Show")
        self.coords = {"x": QSpinBox(), "y": QSpinBox(), "w": QSpinBox(), "h": QSpinBox()}
        self.location = None
        self.npc_list = AutoResizingListWidget()

        # Создаем макет сетки
        layout = QGridLayout(self)

        # Добавляем элементы в сетку
        row = 0  # Начальная строка

        # Первая строка: name, save, is_start_location (если есть), is_shown
        layout.addWidget(QLabel("Name:"), row, 0)
        layout.addWidget(self.name, row, 1)
        layout.addWidget(self.save, row, 2)
        if self.is_start_location is not None:
            layout.addWidget(self.is_start_location, row, 3)
        layout.addWidget(self.is_shown, row, 4)

        # Вторая строка: координаты (если редактирование включено)
        if IS_EDITABLE:
            row += 1
            col = 0
            for key, val in self.coords.items():
                layout.addWidget(QLabel(key), row, col)  # Метка координаты
                col += 1
                val.setMinimum(0)
                val.setMaximum(10000)
                layout.addWidget(val, row, col)  # Поле ввода координаты
                col += 1

        # Третья строка: описание (description)
        row += 1
        layout.addWidget(QLabel("Description:"), row, 0, 1, 1)  # Метка для описания
        layout.addWidget(self.description, row, 1, 1, -1)  # Описание занимает всю оставшуюся ширину

        # Четвертая строка: список NPC (npc_list)
        row += 1
        layout.addWidget(QLabel("NPC List:"), row, 0)  # Метка для списка NPC
        layout.addWidget(self.npc_list, row, 1, 1, -1) 

    def on_location_selected(self, location_id: int) -> None:
        self.location = self.session.query(Location).filter(Location.id == location_id).first()
        if self.location is None:
            return

        self.name.setText(self.location.name)
        self.description.setText(self.location.description)
        tmp = self.location.is_shown if self.location.is_shown is not None else 2
        self.is_start_location.setChecked(tmp == 2) #
        self.is_shown.setChecked(tmp > 0) #
        self.coords["x"].setValue(self.location.offsetX)
        self.coords["y"].setValue(self.location.offsetY)
        self.coords["w"].setValue(self.location.width)
        self.coords["h"].setValue(self.location.height)

        self.set_npcs()


    def on_save(self):
        if self.location is None:
            return
        self.location.name = self.name.text()
        self.location.description = self.description.toHtml()
        self.session.commit()

    def set_npcs(self):
        self.npc_list.clear()
        # for item in self.npc_list.children():
            # self.npc_list.removeItemWidget(item)
        # Получаем условия появления NPC
        npcs_conditions = check_marks_in_condition(
            self.session.query(GameCondition).filter(
                GameCondition.playerActionId == None,
                GameCondition.locationId == self.location.id,
                GameCondition.npcId != None
            ).all()
        )

        appearance = {}
        for npc_c in npcs_conditions:
            if npc_c.npcId in appearance:
                appearance[npc_c.npcId].append(npc_c.text)
            else:
                appearance[npc_c.npcId] = [npc_c.text]
        
        for npc_id in appearance:
            npc = self.session.query(NPC).filter(NPC.id == npc_id).first()
            if npc is not None:
                item = QListWidgetItem(self.npc_list)
                widget = NpcWidget(npc=npc, appearance=appearance[npc.id], location=self.location)
                self.npc_list.setItemWidget(item, widget)
                item.setSizeHint(widget.sizeHint())

