from PyQt5.QtWidgets import QMainWindow, QWidget, QMenu, QMessageBox, QFileDialog, QHBoxLayout, QVBoxLayout, QTabWidget, QMenuBar, QAction, QPushButton
from widgets import MapWidget, ItemListWidget, GlobalMapWidget, NoteListWidget, LocationWidget, NpcListWidget, PlayerListWidget, MapSettingsWidget, EventListWidget
from dialogs import SkillsDialog, SkillHelpDialog
from common import HtmlTextEdit, LogWidget, get_local_ip
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QGuiApplication
import sys
import os
import shutil
from zipfile import ZipFile, ZIP_DEFLATED
from repositories import reset_scenario

from scheme import *


class MainWindow(QMainWindow):
    maps_update = pyqtSignal()

    map_image_saved = pyqtSignal()

    need_to_reload = pyqtSignal()
    map_updated = pyqtSignal()
    characters_updated = pyqtSignal()
    notes_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        global IS_EDITABLE
        self.setWindowTitle(get_local_ip())
        
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("Settings")
        self.checkbox_action = QAction("Editable", self)
        self.checkbox_action.setCheckable(True)
        self.checkbox_action.setChecked(IS_EDITABLE)  
        self.checkbox_action.triggered.connect(changed_manager.change_editable)
        settings_menu.addAction(self.checkbox_action)
        self.open_action = QAction("Open", self)
        self.open_action.triggered.connect(self.open_zip_file)
        settings_menu.addAction(self.open_action)
        self.save_action = QAction("Save", self)
        self.save_action.triggered.connect(self.save_default)
        self.save_action.setDisabled(True)
        self.check_scenario_name()
        settings_menu.addAction(self.save_action)
        self.save_as_action = QAction("Save As", self)
        self.save_as_action.triggered.connect(self.save_as)
        settings_menu.addAction(self.save_as_action)
        self.reset_action = QAction("Reset", self)
        self.reset_action.triggered.connect(self.set_up)
        settings_menu.addAction(self.reset_action)

        scenario_menu = menu_bar.addMenu("Scenario")
        self.skills = QAction("Skills", self)
        self.skills.triggered.connect(self.show_skill_dialog)
        scenario_menu.addAction(self.skills)
        self.reset_scenario_action = QAction("Reset", self)
        self.reset_scenario_action.triggered.connect(self.reset_scenario)
        scenario_menu.addAction(self.reset_scenario_action)

        help_menu = menu_bar.addMenu("Help")
        self.skills_help = QAction("Skills", self)
        self.skills_help.triggered.connect(self.show_help_skill_dialog)
        help_menu.addAction(self.skills_help)

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

        screen = QGuiApplication.screenAt(self.geometry().center())  # Определяем экран, где находится окно
        screen_height = None
        screen_width = None
        if screen:
            screen_geometry = screen.geometry()
            screen_height = screen_geometry.height()
            screen_width = screen_geometry.width()


        self.skill_dialog = SkillsDialog()
        self.skill_help_dialog = SkillHelpDialog()

        self.map_tabs = QTabWidget()
        self.data_tabs = QTabWidget()
        self.button = QPushButton("reload")
        self.button.clicked.connect(self.need_to_reload)
        self.button_char = QPushButton("reload char")
        self.button_char.clicked.connect(self.characters_updated)

        self.global_map = GlobalMapWidget()
        self.map = MapWidget()
        self.intro = HtmlTextEdit(is_fixed=False, max_height=screen_height//4)
        self.map_tabs.addTab(self.global_map, "global map")
        self.map_tabs.addTab(self.map, "map")
        # self.map_tabs.setMaximumSize(QSize(700, 700))
        self.map_tabs.setMaximumHeight(screen_height * 2 // 3 if screen_height else 700)
        self.map_tabs.setMaximumWidth(screen_width // 3 if screen_width else 400)

        self.map_settings = MapSettingsWidget()
        self.location = LocationWidget()
        self.npcs = NpcListWidget()
        self.items = ItemListWidget()
        self.marks = QWidget()
        self.notes = NoteListWidget()
        self.game_events = EventListWidget()
        self.data_tabs.addTab(self.map_settings, "map settings")
        self.data_tabs.addTab(self.location, "location")
        self.data_tabs.addTab(self.npcs, "npcs")
        self.data_tabs.addTab(self.items, "items")
        self.data_tabs.addTab(self.marks, "marks")
        self.data_tabs.addTab(self.notes, "notes")
        self.data_tabs.addTab(self.game_events, "events")

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
        self.global_map.map_object_clicked.connect(self.set_scenemap_focus)
        self.global_map.datetime_changed.connect(self.map.on_datetime_changed)
        self.global_map.datetime_changed.connect(self.player_list.on_datetime_changed)
        self.global_map.datetime_changed.connect(self.game_events.set_time)
        self.global_map.map_image_saved.connect(self.map_image_saved)
        self.map_settings.map_object_updated.connect(self.global_map.on_map_update)

        self.map.map_object_clicked.connect(self.location.on_location_selected)
        self.map.map_object_clicked.connect(self.set_location_focus)
        self.map.map_object_clicked.connect(self.items.set_location)
        self.map.map_image_saved.connect(self.map_image_saved)
        self.map.datetime_changed.connect(self.global_map.on_datetime_changed)
        self.map.datetime_changed.connect(self.player_list.on_datetime_changed)
        self.map.datetime_changed.connect(self.game_events.set_time)
        self.map.map_changed.connect(self.map_settings.on_map_selected)
        self.location.map_object_updated.connect(self.map.on_map_update)

        self.maps_update.connect(self.global_map.on_map_update)
        self.maps_update.connect(self.map.on_map_update)

        self.intro.textChanged.connect(self.on_save)

        self.items.list_changed.connect(self.location.items_list.fill_list)
        self.npcs.list_changed.connect(self.location.npc_list.fill_list)
        
        self.items.list_changed.connect(self.characters_updated)
        self.location.item_list_changed.connect(self.characters_updated)

        self.notes.list_changed.connect(self.notes_updated)
        
        changed_manager.players_changed.connect(self.player_list.fill_list)
        changed_manager.notes_changed.connect(self.notes.fill_list)

        changed_manager.players_changed.connect(self.characters_updated)
        changed_manager.notes_changed.connect(self.notes_updated)

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

    def update_connections(self):
        self.player_list.update_connections()

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

    def save_as(self):
        options = QFileDialog.Options()
        output_zip, _ = QFileDialog.getSaveFileName(self, "Save ZIP File", "", "ZIP Files (*.zip);;All Files (*)", options=options)
        if not output_zip:
            return 

        if not output_zip.endswith('.zip'):
            output_zip += '.zip'
        if self.save_to_zip_file(output_zip):
            globla_map = session.query(GlobalMap).first()
            if globla_map is None:
                return
            globla_map.scenario_name = output_zip.split('/')[-1][:-4]
            globla_map.scenario_file_path = output_zip
            session.commit()
            self.check_scenario_name()
        

    def save_default(self):
        globla_map = session.query(GlobalMap).first()
        if globla_map is None or globla_map.scenario_file_path is None:
            return
        self.save_to_zip_file(globla_map.scenario_file_path)

    def save_to_zip_file(self, output_zip):
        try:
            # Архивируем выбранную папку
            with ZipFile(output_zip, 'w', ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(DEFAULT_DIR):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, DEFAULT_DIR)
                        zipf.write(file_path, arcname)

            QMessageBox.information(self, "Success", f"Folder successfully archived to {output_zip}")
            return True
        except PermissionError:
            QMessageBox.critical(self, "Error", "Permission denied while accessing files.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
        return False

    def check_scenario_name(self):
        globla_map = session.query(GlobalMap).first()
        if globla_map is None:
            return
        self.save_action.setDisabled(globla_map.scenario_name is None)
        if globla_map.scenario_name is not None:
            self.setWindowTitle(f"{globla_map.scenario_name} ({get_local_ip()})")

    def show_help_skill_dialog(self):
        self.skill_help_dialog.show()

    def reset_scenario(self):
        reset_scenario()

    def set_location_focus(self):
        self.data_tabs.setCurrentWidget(self.location)
    
    def set_scenemap_focus(self):
        self.map_tabs.setCurrentWidget(self.map)

