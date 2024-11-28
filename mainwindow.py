from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QMenuBar, QAction, QPushButton
from widgets.map_widget import MapWidget
from widgets.global_map_widget import GlobalMapWidget
from widgets.location_widget import LocationWidget
from widgets.npc_list_widget import NpcListWidget
from widgets.map_settings_widget import MapSettingsWidget
from widgets.player_list_widget import PlayerListWidget
from dialogs.skills_dialog import SkillsDialog
from PyQt5.QtCore import pyqtSignal

from scheme import IS_EDITABLE


class MainWindow(QMainWindow):
    need_to_reload = pyqtSignal()

    def __init__(self):
        super().__init__()
        global IS_EDITABLE
        
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("Settings")
        self.checkbox_action = QAction("Editable", self)
        self.checkbox_action.setCheckable(True)
        self.checkbox_action.setChecked(IS_EDITABLE)  
        self.checkbox_action.triggered.connect(self.on_checkbox_toggled)
        settings_menu.addAction(self.checkbox_action)

        self.skills = QAction("Skills", self)
        self.skills.triggered.connect(self.show_skill_dialog)
        settings_menu.addAction(self.skills)

        self.reset_action = QAction("Reset", self)
        self.reset_action.triggered.connect(self.set_up)
        settings_menu.addAction(self.reset_action)


        self.set_up()

    def set_up(self):
        w = QWidget()
        self.main_layout = QVBoxLayout()
        w.setLayout(self.main_layout)
        self.setCentralWidget(w)

        self.skill_dialog = SkillsDialog()

        self.map_tabs = QTabWidget()
        self.data_tabs = QTabWidget()
        self.button = QPushButton("test")
        self.button.clicked.connect(self.need_to_reload)

        self.global_map = GlobalMapWidget()
        self.map = MapWidget()
        self.map_tabs.addTab(self.global_map, "global map")
        self.map_tabs.addTab(self.map, "map")

        self.map_settings = MapSettingsWidget()
        self.location = LocationWidget()
        self.npcs = NpcListWidget()
        self.items = QWidget()
        self.marks = QWidget()
        self.notes = QWidget()
        self.data_tabs.addTab(self.map_settings, "map settings")
        self.data_tabs.addTab(self.location, "location")
        self.data_tabs.addTab(self.npcs, "npcs")
        self.data_tabs.addTab(self.items, "items")
        self.data_tabs.addTab(self.marks, "marks")
        self.data_tabs.addTab(self.notes, "notes")

        self.player_list = PlayerListWidget()

        tmp_layout = QHBoxLayout()
        self.main_layout.addLayout(tmp_layout)
        tmp_layout.addWidget(self.map_tabs)
        tmp_layout.addWidget(self.data_tabs)
        tmp_layout.addWidget(self.player_list)
        self.main_layout.addWidget(self.button)

        self.global_map.map_changed.connect(self.map_settings.on_map_selected)
        self.global_map.map_changed.connect(self.map.set_current_map)
        self.map_settings.map_object_updated.connect(self.global_map.on_map_update)
        self.map.location_clicked.connect(self.location.on_location_selected)
        self.map.map_changed.connect(self.map_settings.on_map_selected)
        self.location.map_object_updated.connect(self.map.on_map_update)

        self.npcs.npc_list_changed.connect(self.location.set_npcs)

    def on_checkbox_toggled(self, checked):
        global IS_EDITABLE
        IS_EDITABLE = checked
        print(f'{IS_EDITABLE=}')

    def show_skill_dialog(self):
        self.skill_dialog.exec()

    