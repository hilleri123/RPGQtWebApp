from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QComboBox, QHBoxLayout, QListWidget, QPushButton, QLineEdit, QLabel
)
from scheme import *

class SkillsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Управление навыками")

        # Основной макет
        layout = QVBoxLayout(self)

        # Создаем виджет списка
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Поле ввода для нового навыка
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Введите название навыка")
        layout.addWidget(self.input_name)
        self.group_combobox = QComboBox()
        self.group_combobox.addItems(SKILL_GROUP)
        layout.addWidget(self.group_combobox)

        # Кнопки добавления и удаления
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.add_skill)
        
        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(self.delete_skill)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout)

        # Загрузка данных из базы данных
        self.load_skills()

    def load_skills(self):
        """Загружает навыки из базы данных в список."""
        self.list_widget.clear()
        skills = session.query(Skill).all()
        for skill in skills:
            self.list_widget.addItem(f"{skill.name} ({skill.groupName})")

    def add_skill(self):
        name = self.input_name.text().strip()
        group = self.group_combobox.currentText()
        
        if not name:
            return  # Не добавляем пустые строки
        
        new_skill = Skill(name=name, groupName=group)
        
        session.add(new_skill)
        session.commit()
        
        self.input_name.clear()
        
        self.load_skills()

    def delete_skill(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return
        
        for item in selected_items:
            skill_text = item.text()
            skill_name = skill_text.split(" (")[0]
            skill_to_delete = session.query(Skill).filter(Skill.name == skill_name).first()
            if skill_to_delete:
                session.delete(skill_to_delete)
                session.commit()
        
        self.load_skills()
