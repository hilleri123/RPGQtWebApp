from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *


class NpcWidget(QWidget):
    def __init__(self, npc: NPC, appearance: list[str] = None, location: Location = None, parent=None):
        super().__init__(parent)
        self.session = Session()

        loc_dialogs = []
        if location is not None:
            loc_dialogs = check_marks_in_condition(
                self.session.query(GameCondition).filter(
                    GameCondition.playerActionId != None,
                    GameCondition.locationId == location.id,
                    GameCondition.npcId == npc.id
                ).all()
            )
        
        dialogs = check_marks_in_condition(
            self.session.query(GameCondition).filter(
                GameCondition.playerActionId != None,
                GameCondition.locationId == None,
                GameCondition.npcId == npc.id
            ).all()
        )

        # Поля для редактирования
        self.npc_name_field = QLineEdit()  # Поле для имени NPC
        self.appearance_field = QTextEdit()  # Поле для списка внешностей (appearance)
        self.loc_dialogs_list = QListWidget()  # Список локальных диалогов
        self.dialogs_list = QListWidget()  # Список общих диалогов

        # Кнопки для управления диалогами
        self.add_loc_dialog_button = QPushButton("Добавить локальный диалог")
        self.add_loc_dialog_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_dialog_button = QPushButton("Добавить общий диалог")
        self.add_dialog_button.setIcon(QIcon.fromTheme("document-new"))
        self.save_button = QPushButton("Сохранить")
        # self.save_button.clicked.connect(self.save_data)

        # Основной макет
        layout = QVBoxLayout(self)

        # Формы для полей
        form_layout = QFormLayout()
        form_layout.addRow("Имя NPC:", self.npc_name_field)
        form_layout.addRow("Внешности (appearance):", self.appearance_field)

        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)

        # Локальные диалоги
        loc_dialogs_layout = QVBoxLayout()
        loc_dialogs_layout.addWidget(QLabel("Локальные диалоги:"))
        loc_dialogs_layout.addWidget(self.loc_dialogs_list)
        
        loc_buttons_layout = QHBoxLayout()
        loc_buttons_layout.addWidget(self.add_loc_dialog_button)
        
        loc_dialogs_layout.addLayout(loc_buttons_layout)
        
        layout.addLayout(loc_dialogs_layout)

        # Общие диалоги
        dialogs_layout = QVBoxLayout()
        dialogs_layout.addWidget(QLabel("Общие диалоги:"))
        dialogs_layout.addWidget(self.dialogs_list)
        
        dialog_buttons_layout = QHBoxLayout()
        dialog_buttons_layout.addWidget(self.add_dialog_button)
        dialogs_layout.addLayout(dialog_buttons_layout)
        
        layout.addLayout(dialogs_layout)

