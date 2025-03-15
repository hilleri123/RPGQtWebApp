from PyQt5.QtWidgets import QMainWindow, QWidget, QMenu, QMessageBox, QFileDialog, QHBoxLayout, QVBoxLayout, QTabWidget, QMenuBar, QAction, QPushButton
from src.widgets import MapEditor
# from src.dialogs import SkillsDialog
from src.common import HtmlTextEdit, TableWidget
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QGuiApplication
import sys
import os
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

from scheme import *

DEFAULT_DIR = ''

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
        
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("Settings")
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


        # self.skill_dialog = SkillsDialog()
        # self.skill_help_dialog = SkillHelpDialog()

        self.data_tabs = QTabWidget()
        self.button = QPushButton("reload")
        self.button.clicked.connect(self.need_to_reload)
        self.button_char = QPushButton("reload char")
        self.button_char.clicked.connect(self.characters_updated)

        self.map_settings = MapEditor()
        # self.location = LocationWidget()
        # self.npcs = NpcListWidget()
        # self.items = ItemListWidget()
        # self.marks = QWidget()
        # self.notes = NoteListWidget()
        # self.game_events = EventListWidget()
        self.data_tabs.addTab(self.map_settings, "map settings")
        # self.data_tabs.addTab(self.location, "location")
        self.data_tabs.addTab(TableWidget(NPC, QFileDialog), "npcs")
        self.data_tabs.addTab(TableWidget(GameItem, QFileDialog), "items")
        # self.data_tabs.addTab(self.marks, "marks")
        self.data_tabs.addTab(TableWidget(Note, QFileDialog), "notes")
        self.data_tabs.addTab(TableWidget(GameEvent, QFileDialog), "events")


        tmp_layout = QHBoxLayout()
        self.main_layout.addLayout(tmp_layout)
        tmp_tmp_layout = QVBoxLayout()
        tmp_layout.addLayout(tmp_tmp_layout)
        # tmp_tmp_layout.addWidget(self.map_tabs)
        # tmp_tmp_layout.addWidget(self.intro)
        tmp_layout.addWidget(self.data_tabs)
        self.main_layout.addLayout(tmp_layout)
        tmp_tmp_layout = QVBoxLayout()
        tmp_layout.addLayout(tmp_tmp_layout)
        # tmp_tmp_layout.addWidget(self.player_list)
        # tmp_tmp_layout.addWidget(self.logs)
        # self.main_layout.addWidget(self.button)
        # self.main_layout.addWidget(self.button_char)
        
        self.fill()

        # self.intro.textChanged.connect(self.on_save)


    def fill_map_object(self):
        with Session() as session:
            global_map = session.query(GlobalSession).first()
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
        with Session() as session:
            global_map = session.query(GlobalSession).first()
            if global_map is None:
                return
            self.intro.setHtml(global_map.intro)

    def on_save(self):
        with Session() as session:
            global_map = session.query(GlobalSession).first()
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
        with Session() as session:
            options = QFileDialog.Options()
            output_zip, _ = QFileDialog.getSaveFileName(self, "Save ZIP File", "", "ZIP Files (*.zip);;All Files (*)", options=options)
            if not output_zip:
                return 

            if not output_zip.endswith('.zip'):
                output_zip += '.zip'
            if self.save_to_zip_file(output_zip):
                globla_map = session.query(GlobalSession).first()
                if globla_map is None:
                    return
                globla_map.scenario_name = output_zip.split('/')[-1][:-4]
                globla_map.scenario_file_path = output_zip
                session.commit()
                self.check_scenario_name()
        

    def save_default(self):
        with Session() as session:
            globla_map = session.query(GlobalSession).first()
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
        with Session() as session:
            globla_map = session.query(GlobalSession).first()
            if globla_map is None:
                return
            self.save_action.setDisabled(globla_map.scenario_name is None)
            if globla_map.scenario_name is not None:
                self.setWindowTitle(f"{globla_map.scenario_name}")

    def show_help_skill_dialog(self):
        # self.skill_help_dialog.show()
        pass

    def reset_scenario(self):
        pass
        # reset_scenario()

    def set_location_focus(self):
        self.data_tabs.setCurrentWidget(self.location)
    
    def set_scenemap_focus(self):
        # self.map_tabs.setCurrentWidget(self.map)
        pass

