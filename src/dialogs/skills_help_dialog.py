from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QComboBox, QHBoxLayout, QListWidget, QPushButton, QLineEdit, QLabel
)
from scheme import *
import json

class SkillHelpDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Подсчет навыками")

        # Основной макет
        layout = QVBoxLayout(self)

        # Создаем виджет списка
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.load_skills()


    def load_skills(self):
        self.list_widget.clear()
        actions = session.query(PlayerAction).all()
        skills_count = {}
        for action in actions:
            if action.needSkillIdsConditionsJson is None:
                continue
            skill_list = json.loads(action.needSkillIdsConditionsJson)
            for item in skill_list:
                skill_id = None
                if type(item) is list:
                    skill_id = item[0]
                else:
                    skill_id = item
                if skill_id in skills_count:
                    skills_count[skill_id] += 1
                else:
                    skills_count[skill_id] = 1

        skills = session.query(Skill).all()
        for skill in skills:
            if skill.id in skills_count:
                self.list_widget.addItem(f"{skill.name} ({skills_count[skill.id]})")
