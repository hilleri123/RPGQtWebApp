from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QSizePolicy, QApplication, QCheckBox, QListWidgetItem, QLineEdit, QTextEdit, QListWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import pyqtSignal
from scheme import *
from repositories import *
from common import AutoResizingListWidget, BaseListWidget, HtmlTextEdit, BaseListItemWidget, SkillListWidget, icons
from .action_widget import ActionWidget
from dialogs import NPCEditDialog


class NpcDialogList(BaseListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def list_name(self):
        return 'Общие диалоги:'

    def set_npc_id(self, npc_id):
        self.npc_id = npc_id
        self.fill_list()

    def query_list(self) -> list:
        try:
            if self.npc_id is None:
                return []
        except AttributeError:
            return []
        
        return self.session.query(PlayerAction).join(GameCondition).filter(
                GameCondition.playerActionId != None,
                GameCondition.locationId == None,
                GameCondition.npcId == self.npc_id
            ).all()

    def widget_of(self, db_object) -> QWidget:
        return ActionWidget(db_object)
    
    def add_default_element(self):
        action = PlayerAction()
        self.session.add(action)
        self.session.commit()
        # TODO Mark
        c = GameCondition(npcId=self.npc_id, playerActionId=action.id)
        self.session.add(c)
        self.session.commit()


class NpcWidget(BaseListItemWidget):
    def __init__(self, npc: NPC, parent=None, **args):
        super().__init__(npc, parent)
        self.labels = []
        if self.db_object.skillIdsJson is not None:
            self.skill_list = SkillListWidget(json.loads(self.db_object.skillIdsJson))
            self.base_layout.addWidget(self.skill_list)
        if self.db_object.description is not None:
            self.description = HtmlTextEdit()
            self.description.setReadOnly(True)
            self.base_layout.addWidget(self.description)
            self.description.setHtml(self.db_object.description)
            self.labels.append(self.description)

        self.setup(**args)
        self.add_lists(**args)

        self.edit_dialog = NPCEditDialog(npc_id=self.db_object.id)
        
    def fill_first_line(self):
        super().fill_first_line()
        self.npc_is_alive = QCheckBox()
        self.npc_is_alive.setChecked(not self.db_object.isDead)
        self.npc_is_alive.clicked.connect(self.set_alive)
        self.set_alive()
        self.first_line_layout.addWidget(self.npc_is_alive)
        self.edit_npc_button = QPushButton()
        self.edit_npc_button.setIcon(icons.edit_icon())
        self.edit_npc_button.setEnabled(IS_EDITABLE)
        self.edit_npc_button.clicked.connect(self.on_edit_npc)
        self.first_line_layout.addWidget(self.edit_npc_button)

        self.icon = QLabel()
        if self.db_object.path_to_img:
            i = QIcon(f'{NPC_ICONS_DIR}/{self.db_object.path_to_img}')
            self.icon.setPixmap(i.pixmap(16, 16))
        self.first_line_layout.insertWidget(0, self.icon)

    def name(self) -> str:
        return self.db_object.name

    def setup(self, **args):
        pass

    def add_lists(self, **args):
        self.dialogs = []
        self.dialogs_list = NpcDialogList()
        self.dialogs_list.set_npc_id(self.db_object.id)
        self.base_layout.addWidget(self.dialogs_list)

    def on_edit_npc(self):
        self.edit_dialog.exec_()
        self.changed.emit()

    def set_alive(self):
        palette = self.palette()
        if not self.npc_is_alive.isChecked():
            palette.setColor(QPalette.Background, QColor(255, 0, 0, 127))
        else:
            palette = QApplication.palette()
        self.setPalette(palette)
        self.on_save()

    def on_save(self):
        self.db_object.isDead = not self.npc_is_alive.isChecked()
        super().on_save()
