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

        default_button = QPushButton("Заполнить стандартными")
        default_button.clicked.connect(self.fill_default)

        layout.addWidget(default_button)

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

    def fill_default(self):
        skills = {
            "Анализ текста": SKILL_GROUP[0],
            "Антропология": SKILL_GROUP[0],
            "Археология": SKILL_GROUP[0],
            "Архитектура": SKILL_GROUP[0],
            "Аудит": SKILL_GROUP[0],
            "Естествознание": SKILL_GROUP[0],
            "Знание языков": SKILL_GROUP[0],
            "Искусствоведение": SKILL_GROUP[0],
            "Исследовательская работа": SKILL_GROUP[0],
            "История": SKILL_GROUP[0],
            "Лингвистика": SKILL_GROUP[0],
            "Оккультные науки": SKILL_GROUP[0],
            "Судебная психология": SKILL_GROUP[0],
            "Юриспруденция": SKILL_GROUP[0],
            "Эрудиция": SKILL_GROUP[0],
            "Анализ документов": SKILL_GROUP[1],
            "Астрономия": SKILL_GROUP[1],
            "Баллистика": SKILL_GROUP[1],
            "Дактилоскопия": SKILL_GROUP[1],
            "Извлечение данных": SKILL_GROUP[1],
            "Криптография": SKILL_GROUP[1],
            "Патология": SKILL_GROUP[1],
            "Прикладная физика": SKILL_GROUP[1],
            "Сапёрное дело": SKILL_GROUP[1],
            "Сбор улик": SKILL_GROUP[1],
            "Судебная антропология": SKILL_GROUP[1],
            "Фотография": SKILL_GROUP[1],
            "Химия": SKILL_GROUP[1],
            "Электронная слежка": SKILL_GROUP[1],
            "Бюрократия": SKILL_GROUP[2],
            "Ведение допроса": SKILL_GROUP[2],
            "Ведение переговоров": SKILL_GROUP[2],
            "Запугивание": SKILL_GROUP[2],
            "Лесть": SKILL_GROUP[2],
            "Полицейский жаргон": SKILL_GROUP[2],
            "Притворство": SKILL_GROUP[2],
            "Проницательность": SKILL_GROUP[2],
            "Уличное чутьё": SKILL_GROUP[2],
            "Успокаивание": SKILL_GROUP[2],
            "Флирт": SKILL_GROUP[2],
            "Атлетика": SKILL_GROUP[3],
            "Вождение": SKILL_GROUP[3],
            "Воровство": SKILL_GROUP[3],
            "Ободрение": SKILL_GROUP[3],
            "Драка": SKILL_GROUP[3],
            "Здоровье": SKILL_GROUP[3],
            "Механика": SKILL_GROUP[3],
            "Первая помощь": SKILL_GROUP[3],
            "Предусмотрительность": SKILL_GROUP[3],
            "Проникновение": SKILL_GROUP[3],
            "Самообладание": SKILL_GROUP[3],
            "Слежка": SKILL_GROUP[3],
            "Стрельба": SKILL_GROUP[3],
        }
        for skill_name, group in skills.items():
            try:
                new_skill = Skill(name=skill_name, groupName=group)
                session.add(new_skill)
                session.commit()
            except:
                pass

        self.load_skills()

