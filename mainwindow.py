from PyQt5.QtWidgets import QMainWindow, QWidget, QMenu, QMessageBox, QFileDialog, QHBoxLayout, QVBoxLayout, QTabWidget, QMenuBar, QAction, QPushButton
from widgets import MapWidget, ItemListWidget, GlobalMapWidget, LocationWidget, NpcListWidget, PlayerListWidget, MapSettingsWidget
from dialogs import SkillsDialog
from common import AutoResizingTextEdit, LogWidget, get_local_ip
from PyQt5.QtCore import pyqtSignal, QSize
import sys
import os
import shutil
from zipfile import ZipFile

from scheme import *


class MainWindow(QMainWindow):
    maps_update = pyqtSignal()

    map_image_saved = pyqtSignal()

    need_to_reload = pyqtSignal()
    map_updated = pyqtSignal()
    characters_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        global IS_EDITABLE
        self.setWindowTitle(get_local_ip())
        
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("Settings")
        self.checkbox_action = QAction("Editable", self)
        self.checkbox_action.setCheckable(True)
        self.checkbox_action.setChecked(IS_EDITABLE)  
        self.checkbox_action.triggered.connect(self.on_checkbox_toggled)
        settings_menu.addAction(self.checkbox_action)
        self.open_action = QAction("Open", self)
        self.open_action.triggered.connect(self.open_zip_file)
        settings_menu.addAction(self.open_action)
        self.reset_action = QAction("Reset", self)
        self.reset_action.triggered.connect(self.set_up)
        settings_menu.addAction(self.reset_action)

        scenario_menu = menu_bar.addMenu("Scenario")
        self.skills = QAction("Skills", self)
        self.skills.triggered.connect(self.show_skill_dialog)
        scenario_menu.addAction(self.skills)

        self.map_objects_menu = menu_bar.addMenu("Map objects")
        self.fill_map_object()

        self.set_up()

    def set_up(self):
        if self.centralWidget():
            self.centralWidget().deleteLater()
            self.setCentralWidget(None)
        w = QWidget()
        self.main_layout = QVBoxLayout()
        w.setLayout(self.main_layout)
        self.setCentralWidget(w)

        self.skill_dialog = SkillsDialog()

        self.map_tabs = QTabWidget()
        self.data_tabs = QTabWidget()
        self.button = QPushButton("reload")
        self.button.clicked.connect(self.need_to_reload)
        self.button_char = QPushButton("reload char")
        self.button_char.clicked.connect(self.characters_updated)

        self.global_map = GlobalMapWidget()
        self.map = MapWidget()
        self.intro = AutoResizingTextEdit()
        self.map_tabs.addTab(self.global_map, "global map")
        self.map_tabs.addTab(self.map, "map")
        self.map_tabs.setMaximumSize(QSize(700, 700))

        self.map_settings = MapSettingsWidget()
        self.location = LocationWidget()
        self.npcs = NpcListWidget()
        self.items = ItemListWidget()
        self.marks = QWidget()
        self.notes = QWidget()
        self.data_tabs.addTab(self.map_settings, "map settings")
        self.data_tabs.addTab(self.location, "location")
        self.data_tabs.addTab(self.npcs, "npcs")
        self.data_tabs.addTab(self.items, "items")
        self.data_tabs.addTab(self.marks, "marks")
        self.data_tabs.addTab(self.notes, "notes")

        self.player_list = PlayerListWidget()
        self.logs = LogWidget()

        tmp_layout = QHBoxLayout()
        self.main_layout.addLayout(tmp_layout)
        tmp_tmp_layout = QVBoxLayout()
        tmp_layout.addLayout(tmp_tmp_layout)
        tmp_tmp_layout.addWidget(self.map_tabs)
        tmp_tmp_layout.addWidget(self.intro)
        tmp_layout.addWidget(self.data_tabs)
        self.main_layout.addLayout(tmp_layout)
        tmp_tmp_layout = QVBoxLayout()
        tmp_layout.addLayout(tmp_tmp_layout)
        tmp_tmp_layout.addWidget(self.player_list)
        tmp_tmp_layout.addWidget(self.logs)
        self.main_layout.addWidget(self.button)
        self.main_layout.addWidget(self.button_char)
        
        self.fill()

        self.global_map.map_changed.connect(self.map_settings.on_map_selected)
        self.global_map.map_changed.connect(self.map.set_current_map)
        self.global_map.map_image_saved.connect(self.map_image_saved)
        self.map_settings.map_object_updated.connect(self.global_map.on_map_update)

        self.map.location_clicked.connect(self.location.on_location_selected)
        self.map.map_image_saved.connect(self.map_image_saved)
        self.map.location_clicked.connect(self.items.set_location)
        self.map.map_changed.connect(self.map_settings.on_map_selected)
        self.location.map_object_updated.connect(self.map.on_map_update)

        self.maps_update.connect(self.global_map.on_map_update)
        self.maps_update.connect(self.map.on_map_update)

        self.intro.textChanged.connect(self.on_save)

        self.items.item_list_changed.connect(self.location.set_items)
        self.npcs.npc_list_changed.connect(self.location.set_npcs)

    def fill_map_object(self):
        session = Session()
        global_map = session.query(GlobalMap).first()
        if global_map is None:
            return
        def add_actions_to_menu(menu: QMenu, map_objects: list[MapObjectPolygon]):
            for map_object in map_objects:
                action = QAction(map_object.name, self)
                action.setCheckable(True)
                action.setChecked(map_object.is_shown)
                action.triggered.connect(lambda checked, mo=map_object: self.toggle_map_object(mo))
                menu.addAction(action)

        global_menu = self.map_objects_menu.addMenu(f"G: {global_map.name}")
        add_actions_to_menu(
            global_menu, 
            session.query(MapObjectPolygon).filter(MapObjectPolygon.global_map_id == global_map.id).all(),
            )
        for scene_map in session.query(SceneMap).all():
            scene_map_menu = self.map_objects_menu.addMenu(scene_map.name)
            add_actions_to_menu(
                scene_map_menu, 
                session.query(MapObjectPolygon).filter(MapObjectPolygon.map_id == scene_map.id).all(),
                )

    def toggle_map_object(self, map_object: MapObjectPolygon):
        session = Session()
        map_object.is_shown = not map_object.is_shown
        session.commit()
        self.maps_update.emit()

    def on_checkbox_toggled(self, checked):
        global IS_EDITABLE
        IS_EDITABLE = checked
        print(f'{IS_EDITABLE=}')

    def show_skill_dialog(self):
        self.skill_dialog.exec()

    def update_map(self): # почему-то не работает
        self.maps_update.emit()

    def update_character_stat(self, character_id, stats):
        self.logs.log_stat_change(character_id, stats)

    def update_character_item(self, item_id, from_player, to_player, to_location_id):
        self.logs.log_move_item(item_id, from_player, to_player, to_location_id)
        self.characters_updated.emit()

    def fill(self):
        session = Session()
        global_map = session.query(GlobalMap).first()
        if global_map is None:
            return
        self.intro.setHtml(global_map.intro)

    def on_save(self):
        session = Session()
        global_map = session.query(GlobalMap).first()
        if global_map is None:
            return
        global_map.intro = self.intro.toHtml()
        session.commit()
    
    def open_zip_file(self):
        # Открываем файловый диалог для выбора ZIP-архива
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open ZIP File", "", "ZIP Files (*.zip);;All Files (*)", options=options)
        
        if not fileName:
            return 
        try:
            # Удаляем все содержимое в DEFAULT_PATH
            if os.path.exists(DEFAULT_DIR):
                shutil.rmtree(DEFAULT_DIR)
            os.makedirs(DEFAULT_DIR)

            # Разархивируем выбранный архив в DEFAULT_PATH
            with ZipFile(fileName, 'r') as zip_ref:
                zip_ref.extractall(DEFAULT_DIR)

            QMessageBox.information(self, "Success", f"Archive extracted to {DEFAULT_DIR}")
            self.set_up()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
