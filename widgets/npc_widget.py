from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *
from common import AutoResizingTextEdit


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
        # Основной макет
        layout = QVBoxLayout(self)

        # Формы для полей
        tmp = QHBoxLayout()
        self.npc_name_field = QLineEdit()  # Поле для имени NPC
        self.npc_name_field.setText(npc.name)
        self.npc_name_field.setReadOnly(True)
        tmp.addWidget(self.npc_name_field)
        self.edit_npc_button = QPushButton()
        self.edit_npc_button.setIcon(QIcon.fromTheme("preferences-system"))
        self.edit_npc_button.setEnabled(IS_EDITABLE)
        self.edit_npc_button.clicked.connect(self.on_edit_npc)
        tmp.addWidget(self.edit_npc_button)
        self.add_loc_dialog_button = QPushButton()
        self.add_loc_dialog_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_loc_dialog_button.setEnabled(IS_EDITABLE)
        self.add_loc_dialog_button.clicked.connect(self.on_add_loc_dialog)
        tmp.addWidget(self.add_loc_dialog_button)
        layout.addLayout(tmp)

        # TODO редактировать appearance
        if appearance is not None:
            self.appearance_field = AutoResizingTextEdit()  # Поле для списка внешностей (appearance)
            self.appearance_field.setText('; '.join(appearance))
            self.appearance_field.setReadOnly(True)
            layout.addWidget(self.appearance_field)

        self.loc_dialogs_list = QListWidget()  # Список локальных диалогов
        self.dialogs_list = QListWidget()  # Список общих диалогов

        # Кнопки для управления диалогами
        # self.add_dialog_button = QPushButton("Добавить общий диалог")
        # self.add_dialog_button.setIcon(QIcon.fromTheme("document-new"))
        # self.save_button = QPushButton("Сохранить")
        # self.save_button.clicked.connect(self.save_data)

        # Локальные диалоги
        layout.addWidget(QLabel("Локальные диалоги:"))
        layout.addWidget(self.loc_dialogs_list)

        # Общие диалоги
        layout.addWidget(QLabel("Общие диалоги:"))
        layout.addWidget(self.dialogs_list)


    def on_edit_npc(self):
        pass #TODO


    def on_add_loc_dialog(self):
        pass #TODO

