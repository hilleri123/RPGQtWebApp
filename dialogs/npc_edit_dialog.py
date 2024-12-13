from PyQt5.QtWidgets import (
    QApplication, QDialog, QComboBox, QSpinBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QDateTimeEdit, QPushButton, QListWidget, QListWidgetItem, QSpinBox
)
from PyQt5.QtCore import Qt
from scheme import *
from common import AutoResizingListWidget
from common.html_text_edit_widget import HtmlTextEdit
import sqlalchemy
import json



class NPCEditDialog(QDialog):
    def __init__(self, npc_id=None):
        super().__init__()

        self.setWindowTitle("Редактирование персонажа")

        layout = QVBoxLayout(self)

        self.description = HtmlTextEdit()

        layout.addWidget(QLabel("Описание:"))
        layout.addWidget(self.description)

        self.skills_list_widget = AutoResizingListWidget()
        layout.addWidget(QLabel("Навыки:"))
        layout.addWidget(self.skills_list_widget)

        # Кнопки добавления и удаления навыков
        button_layout = QHBoxLayout()
        
        add_skill_button = QPushButton("Добавить навык")
        add_skill_button.clicked.connect(self.add_skill)

        self.group_combobox = QComboBox()
        self.group_combobox.addItems(SKILL_GROUP)
        self.group_combobox.currentIndexChanged.connect(self.on_group_selected)
        self.group_name = SKILL_GROUP[0]
        self.skill_combobox = QComboBox()
        self.skill_value = QSpinBox()

        remove_skill_button = QPushButton("Удалить навык")
        remove_skill_button.clicked.connect(self.remove_skill)

        button_layout.addWidget(self.group_combobox)
        button_layout.addWidget(self.skill_combobox)
        button_layout.addWidget(self.skill_value)
        button_layout.addWidget(add_skill_button)
        button_layout.addWidget(remove_skill_button)
        
        layout.addLayout(button_layout)

        self.json_skills = []
        self.npc_id = npc_id
        self.npc = None
        if npc_id is not None:
            self.load_npc()
        
        self.fill_combobox()

        self.connect_all()

    def load_npc(self):
        self.npc = session.query(NPC).get(self.npc_id)
        
        if not self.npc:
            return
        
        self.description.setHtml(self.npc.description)
        self.load_stats()

    def load_stats(self):
        self.skills_list_widget.clear()


        skills = self.npc.skillIdsJson
        if skills is None:
            return
        self.json_skills = json.loads(skills)
        for skill in self.json_skills:
            txt = ""
            if type(skill) is int:
                db_skill = session.query(Skill).get(skill)
                if db_skill is None:
                    continue
                txt = db_skill.name
            else:
                db_skill = session.query(Skill).get(skill[0])
                if db_skill is None:
                    continue
                txt = f'{db_skill.name}: {skill[1]}'
            item_widget = QListWidgetItem(self.skills_list_widget)
            widget = QLabel(txt)
            self.skills_list_widget.setItemWidget(item_widget, widget)

    def fill_combobox(self):
        self.skill_combobox.clear()
        skills = session.query(Skill).filter(Skill.groupName == self.group_name).all()

        for skill in skills:
            self.skill_combobox.addItem(skill.name, skill.id)

    def on_group_selected(self, item):
        self.group_name = SKILL_GROUP[item]
        self.fill_combobox()

    def add_skill(self):
        skill_id = self.skill_combobox.currentData()
        skill_value = self.skill_value.value()
        if skill_value == 0:
            self.json_skills.append(skill_id)
        else:
            self.json_skills.append((skill_id, skill_value))
        self.npc.skillIdsJson = json.dumps(self.json_skills)
        session.commit()

        self.load_stats()
        self.fill_combobox()

    def remove_skill(self):
        selected_items = self.skills_list_widget.selectedItems()
        if not selected_items:
            return
        
        pos_to_del = []
        for item in selected_items:
            pos_to_del.append(self.skills_list_widget.indexFromItem(item))

        pos_to_del = sorted(pos_to_del)
        for pos in pos_to_del[::-1]:
            self.json_skills.pop(pos.row())
        self.npc.skillIdsJson = json.dumps(self.json_skills)
        session.commit()
        
        self.load_stats()
        self.fill_combobox()

    def connect_all(self):
        self.description.textChanged.connect(self.on_save)

    def disconnect_all(self):
        self.description.textChanged.disconnect(self.on_save)
        
    def on_save(self):
        self.npc.description = self.description.toHtml()
        session.commit()