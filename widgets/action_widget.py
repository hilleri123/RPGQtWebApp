from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QComboBox, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from common import SkillListWidget, HtmlTextEdit, BaseListItemWidget, icons
from scheme import *
from dialogs import ActionEditDialog
from datetime import datetime, time, timedelta
import json


class ActionWidget(BaseListItemWidget):
    def __init__(self, db_object=None, parent=None):
        super().__init__(db_object=db_object, parent=parent)

        self.skill_list = SkillListWidget([] if self.db_object is None else json.loads(self.db_object.needSkillIdsConditionsJson))
        self.first_line_layout.insertWidget(0, self.skill_list)

        self.first_line_layout.insertStretch(1)

        activate_all = QPushButton()
        activate_all.setIcon(icons.all_players())
        activate_all.clicked.connect(self.on_activate_all)
        self.first_line_layout.addWidget(activate_all)

        activate_select = QPushButton()
        activate_select.setIcon(icons.select_players())
        activate_select.clicked.connect(self.on_activate_select)
        self.first_line_layout.addWidget(activate_select)

        add_button = QPushButton()
        add_button.setIcon(icons.edit_icon())
        add_button.clicked.connect(self.edit_action)
        self.first_line_layout.addWidget(add_button)

        self.description = HtmlTextEdit()
        self.description.setReadOnly(True)
        self.base_layout.addWidget(self.description)

        if self.db_object is not None:
            self.description.setHtml(self.db_object.description)

    def edit_action(self):
        dialog = ActionEditDialog(self.db_object.id)
        dialog.exec()
        action = session.query(PlayerAction).get(self.db_object.id)
        self.description.setHtml(action.description)
        self.skill_list.load_skills()

    def on_activate(self, players):
        self.db_object.is_activated = True
        if self.db_object.add_time_secs is not None:
            for player in players:
                player.time += timedelta(seconds=self.db_object.add_time_secs)
        self.session.commit()
        print('!')

        self.changed.emit()
        # TODO сделать на активацию две кнопки

    def on_activate_all(self):
        self.on_activate(session.query(PlayerCharacter).all())

    def on_activate_select(self):
        pass

    def name(self):
        return None
    
    def is_hidden(self):
        return self.db_object.is_activated
