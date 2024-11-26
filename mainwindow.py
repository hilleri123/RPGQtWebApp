from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from map_widget import MapWidget
from location_widget import LocationWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        w = QWidget()
        self.main_layout = QVBoxLayout()
        w.setLayout(self.main_layout)
        self.setCentralWidget(w)
        self.button = QPushButton("test")
        self.map = MapWidget()
        self.location = LocationWidget()
        tmp_layout = QHBoxLayout()
        self.main_layout.addLayout(tmp_layout)
        tmp_layout.addWidget(self.map)
        tmp_layout.addWidget(self.location)
        self.main_layout.addWidget(self.button)

        self.map.location_clicked.connect(self.location.on_location_selected)
