from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox, QHBoxLayout, QListWidget, QPushButton, QLineEdit, QLabel
)
from scheme import *
from PyQt5.QtGui import QIcon
from dialogs.action_edit_dialog import ActionEditDialog
import json

class SkillListWidget(QWidget):
    def __init__(self, action_id=None):
        super().__init__()
        self.action_id = action_id
        # Основной макет
        self.skill_layout = QHBoxLayout(self)

        self.load_skills()

    def load_skills(self):
        while self.skill_layout.count():
            item = self.skill_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  # Удаляем виджет
            else:
                del item

        action = session.query(PlayerAction).get(self.action_id)
        if action is None:
            return
        skills = action.needSkillIdsConditionsJson
        if skills is None:
            return
        skills = json.loads(skills)
        for skill in skills:
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
                txt = f'{db_skill.name} {skill[1]}'
            self.skill_layout.addWidget(QLabel(txt))

