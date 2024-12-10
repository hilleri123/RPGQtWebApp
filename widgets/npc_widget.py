from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QSizePolicy, QApplication, QCheckBox, QListWidgetItem, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *
from common import AutoResizingListWidget, BaseListItemWidget
from .action_widget import ActionWidget


class NpcWidget(BaseListItemWidget):
    def __init__(self, npc: NPC, parent=None, **args):
        super().__init__(npc, parent)
        self.labels = []
        self.setup(**args)
        self.add_lists(**args)
        
    def fill_first_line(self):
        super().fill_first_line()
        self.npc_is_alive = QCheckBox()
        self.npc_is_alive.setChecked(not self.db_object.isDead)
        self.npc_is_alive.clicked.connect(self.set_alive)
        self.set_alive()
        self.first_line_layout.addWidget(self.npc_is_alive)
        self.edit_npc_button = QPushButton()
        self.edit_npc_button.setIcon(QIcon.fromTheme("preferences-system"))
        self.edit_npc_button.setEnabled(IS_EDITABLE)
        self.edit_npc_button.clicked.connect(self.on_edit_npc)
        self.first_line_layout.addWidget(self.edit_npc_button)
        self.add_dialog_button = QPushButton()
        self.add_dialog_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_dialog_button.setEnabled(IS_EDITABLE)
        self.add_dialog_button.clicked.connect(self.on_add_dialog)
        self.first_line_layout.addWidget(self.add_dialog_button)

    def name(self) -> str:
        return self.db_object.name

    def setup(self, **args):
        pass

    def add_lists(self, **args):
        self.dialogs = []
        self.dialogs_list = AutoResizingListWidget()
        self.labels.append(QLabel("Общие диалоги:"))
        self.base_layout.addWidget(self.labels[-1])
        self.base_layout.addWidget(self.dialogs_list)
        self.dialogs_fill()


    def dialogs_fill(self):
        self.dialogs_list.clear()

        self.dialogs = check_marks_in_condition(
            self.session.query(GameCondition).filter(
                GameCondition.playerActionId != None,
                GameCondition.locationId == None,
                GameCondition.npcId == self.db_object.id
            ).all()
        )

        for dialog in self.dialogs:
            item = QListWidgetItem(self.dialogs_list)
            widget = ActionWidget(action_id=dialog.playerActionId)
            widget.deleted.connect(self.dialogs_fill)
            self.dialogs_list.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

    def on_edit_npc(self):
        pass #TODO

    def on_add_dialog(self):
        a = PlayerAction()
        self.session.add(a)
        self.session.commit()
        c = GameCondition(
            playerActionId=a.id,
            npcId = self.db_object.id
            )
        self.session.add(c)
        self.session.commit()
        
        self.dialogs_fill()

    def set_alive(self):
        palette = self.palette()
        if not self.npc_is_alive.isChecked():
            palette.setColor(QPalette.Background, QColor(255, 0, 0, 127))
        else:
            palette = QApplication.palette()
        self.setPalette(palette)

