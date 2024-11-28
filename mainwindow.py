from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QMenuBar, QAction, QPushButton
from widgets.map_widget import MapWidget
from widgets.global_map_widget import GlobalMapWidget
from widgets.location_widget import LocationWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        w = QWidget()
        self.main_layout = QVBoxLayout()
        w.setLayout(self.main_layout)
        self.setCentralWidget(w)
        self.map_tabs = QTabWidget()
        self.data_tabs = QTabWidget()
        self.button = QPushButton("test")

        self.global_map = GlobalMapWidget()
        self.map = MapWidget()
        self.map_tabs.addTab(self.global_map)
        self.map_tabs.addTab(self.map)

        self.map_settings = QWidget()
        self.location = LocationWidget()
        self.npcs = QWidget()
        self.items = QWidget()
        self.merks = QWidget()
        self.notes = QWidget()
        self.data_tabs.addTab(self.map_settings)
        self.data_tabs.addTab(self.location)
        self.data_tabs.addTab(self.npcs)
        self.data_tabs.addTab(self.items)
        self.data_tabs.addTab(self.merks)
        self.data_tabs.addTab(self.notes)

        tmp_layout = QHBoxLayout()
        self.main_layout.addLayout(tmp_layout)
        tmp_layout.addWidget(self.map_tabs)
        tmp_layout.addWidget(self.data_tabs)
        self.main_layout.addWidget(self.button)

        self.map.location_clicked.connect(self.location.on_location_selected)
        self.location.location_updated.connect(self.map.on_loc_update)
