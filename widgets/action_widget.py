from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QComboBox, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from common import SkillListWidget
from scheme import *
from dialogs import ActionEditDialog


class ActionWidget(QWidget):
    deleted = pyqtSignal()

    def __init__(self, action_id, parent=None):
        super().__init__(parent)
        self.action_id = action_id

        layout = QVBoxLayout(self)
        tmp = QHBoxLayout()
        layout.addLayout(tmp)

        self.skill_list = SkillListWidget(self.action_id)
        tmp.addWidget(self.skill_list)

        tmp.addStretch()

        add_button = QPushButton()
        add_button.setIcon(QIcon.fromTheme("preferences-system"))
        add_button.clicked.connect(self.edit_action)
        tmp.addWidget(add_button)

        remove_button = QPushButton()
        remove_button.setIcon(QIcon.fromTheme("list-remove"))
        remove_button.clicked.connect(self.delete_action)
        tmp.addWidget(remove_button)

        self.description = QLabel()
        layout.addWidget(self.description)

        action = session.query(PlayerAction).get(self.action_id)
        if action is not None:
            self.description.setText(action.description)

    def edit_action(self):
        dialog = ActionEditDialog(self.action_id)
        dialog.exec()
        action = session.query(PlayerAction).get(self.action_id)
        self.description.setText(action.description)
        self.skill_list.load_skills()

    def delete_action(self):
        action = session.query(PlayerAction).get(self.action_id)
        session.delete(action)
        session.commit()

        self.deleted.emit()
