from PyQt5.QtWidgets import (
    QApplication, QDialog, QComboBox, QSpinBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QDateTimeEdit, QPushButton, QListWidget, QListWidgetItem, QSpinBox
)
from PyQt5.QtCore import Qt
from common.html_text_edit_widget import HtmlTextEdit
from scheme import *
import sqlalchemy

class PlayerCharacterDialog(QDialog):
    def __init__(self, character_id=None):
        super().__init__()

        self.setWindowTitle("Редактирование персонажа")

        layout = QVBoxLayout(self)

        self.name_edit = QLineEdit()
        self.short_desc_edit = QLineEdit()
        self.story_edit = HtmlTextEdit()
        self.time_edit = QDateTimeEdit()

        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_edit)

        layout.addWidget(QLabel("Краткое описание:"))
        layout.addWidget(self.short_desc_edit)

        layout.addWidget(QLabel("История:"))
        layout.addWidget(self.story_edit)

        tmp_layout = QHBoxLayout()
        self.stats_list_widget = QListWidget()
        self.count_label = QLabel()
        tmp_layout.addWidget(QLabel("Навыки:"))
        tmp_layout.addWidget(self.count_label)
        layout.addLayout(tmp_layout)
        layout.addWidget(self.stats_list_widget)

        # Кнопки добавления и удаления навыков
        button_layout = QHBoxLayout()
        
        add_skill_button = QPushButton("Добавить навык")
        add_skill_button.clicked.connect(self.add_stat)

        self.group_combobox = QComboBox()
        self.group_combobox.addItems(SKILL_GROUP)
        self.group_combobox.currentIndexChanged.connect(self.on_group_selected)
        self.group_name = SKILL_GROUP[0]
        self.skill_combobox = QComboBox()
        self.skill_value = QSpinBox()

        remove_skill_button = QPushButton("Удалить навык")
        remove_skill_button.clicked.connect(self.remove_stat)

        button_layout.addWidget(self.group_combobox)
        button_layout.addWidget(self.skill_combobox)
        button_layout.addWidget(self.skill_value)
        button_layout.addWidget(add_skill_button)
        button_layout.addWidget(remove_skill_button)
        
        layout.addLayout(button_layout)

        self.character_id = character_id
        self.character_data = None
        if character_id is not None:
            self.load_character()
        
        self.fill_combobox()

        self.connect_all()

    def load_character(self):
        self.character_data = session.query(PlayerCharacter).filter_by(id=self.character_id).first()
        
        if not self.character_data:
            return
        
        self.name_edit.setText(self.character_data.name or "")
        self.short_desc_edit.setText(self.character_data.shortDesc or "")
        self.story_edit.setHtml(self.character_data.story or "")
        self.load_stats()

    def load_stats(self):
        count_stats = 0
        self.stats_list_widget.clear()
        for stat, skill in session.query(Stat, Skill).join(Skill).filter(Stat.characterId == self.character_id).all():
            item_text = f"{skill.name}: {stat.initValue}"
            count_stats += stat.initValue
            item_widget = QListWidgetItem(item_text)
            item_widget.setData(Qt.UserRole, stat)  # Сохраняем объект Stat в элементе списка
            self.stats_list_widget.addItem(item_widget)
        self.count_label.setText(str(count_stats))

    def fill_combobox(self):
        self.skill_combobox.clear()
        subquery = sqlalchemy.select(1).where(
                (Stat.skillId == Skill.id) &  # Предположим, что есть связь между Skill и Stat через skill_id
                (Stat.characterId == self.character_id)
            )
        skills = session.query(Skill).filter(~sqlalchemy.exists(subquery))\
            .filter(Skill.groupName == self.group_name)\
            .all()

        for skill in skills:
            self.skill_combobox.addItem(skill.name, skill.id)

    def on_group_selected(self, item):
        self.group_name = SKILL_GROUP[item]
        self.fill_combobox()

    def add_stat(self):
        try:
            skill_id = self.skill_combobox.currentData()
            skill_value = self.skill_value.value()
            stat = Stat(characterId=self.character_id, skillId=skill_id, initValue=skill_value, value=skill_value)
            session.add(stat)
            session.commit()
            self.load_stats()
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
        self.fill_combobox()

    def remove_stat(self):
        selected_items = self.stats_list_widget.selectedItems()
        if not selected_items:
            return
        
        for item in selected_items:
            skill_text = item.text()
            skill_name = skill_text.split(": ")[0]
            stat_to_delete = session.query(Stat).join(Skill).filter(Stat.characterId == self.character_id).filter(Skill.name == skill_name).first()
            if stat_to_delete:
                session.delete(stat_to_delete)
                session.commit()
        
        self.load_stats()
        self.fill_combobox()

    def connect_all(self):
        self.name_edit.textChanged.connect(self.on_save)
        self.short_desc_edit.textChanged.connect(self.on_save)
        self.story_edit.textChanged.connect(self.on_save)

    def disconnect_all(self):
        self.name_edit.textChanged.disconnect(self.on_save)
        self.short_desc_edit.textChanged.disconnect(self.on_save)
        self.story_edit.textChanged.disconnect(self.on_save)
        
    def on_save(self):
        self.character_data.name = self.name_edit.text()
        self.character_data.shortDesc = self.short_desc_edit.text()
        self.character_data.story = self.story_edit.toHtml()
        session.commit()