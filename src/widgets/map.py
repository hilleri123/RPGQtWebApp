from PyQt5.QtWidgets import QScrollArea, QFormLayout, QCheckBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint
from scheme import *
import json


class MapEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.polygon_points = []
        self.map_image = None

        self.layoutt = QVBoxLayout()
        self.setLayout(self.layoutt)

        self.image_label = QLabel()  
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(True)
        self.layoutt.addWidget(self.scroll_area)

        self.load_button = QPushButton("Загрузить карту")
        self.load_button.clicked.connect(self.load_map_image)
        self.layoutt.addWidget(self.load_button)

        self.create_polygon_button = QPushButton("Создать полигон")
        self.create_polygon_button.clicked.connect(self.start_creating_polygon)
        self.layoutt.addWidget(self.create_polygon_button)

        self.add_location_button = QPushButton("Добавить локацию")
        self.add_location_button.clicked.connect(self.add_location)
        self.layoutt.addWidget(self.add_location_button)

        self.location_layout = QVBoxLayout()
        self.location_name_input = QLineEdit()
        self.location_description_input = QTextEdit()
        self.location_leads_to_input = QLineEdit()
        self.location_layout.addWidget(QLabel("Имя локации"))
        self.location_layout.addWidget(self.location_name_input)
        self.location_layout.addWidget(QLabel("Описание локации"))
        self.location_layout.addWidget(self.location_description_input)
        self.location_layout.addWidget(QLabel("Ведет к"))
        self.location_layout.addWidget(self.location_leads_to_input)

        self.location_widget = QWidget()
        self.location_widget.setLayout(self.location_layout)

        self.polygon_layout = QFormLayout()
        self.polygon_name_input = QLineEdit()
        self.polygon_color_input = QLineEdit()
        self.polygon_is_shown_checkbox = QCheckBox()
        self.polygon_is_filled_checkbox = QCheckBox()
        self.polygon_is_line_checkbox = QCheckBox()

        self.polygon_layout.addRow(QLabel("Имя полигона"), self.polygon_name_input)
        self.polygon_layout.addRow(QLabel("Цвет полигона"), self.polygon_color_input)
        self.polygon_layout.addRow(QLabel("Отображать"), self.polygon_is_shown_checkbox)
        self.polygon_layout.addRow(QLabel("Заливка"), self.polygon_is_filled_checkbox)
        self.polygon_layout.addRow(QLabel("Линия"), self.polygon_is_line_checkbox)

        self.polygon_widget = QWidget()
        self.polygon_widget.setLayout(self.polygon_layout)

        tmplayout = QHBoxLayout()        
        tmplayout.addWidget(self.polygon_widget)

        tmplayout.addWidget(self.location_widget)
        self.layoutt.addLayout(tmplayout)

        self.image_label.mousePressEvent = self.get_mouse_press_event

    def load_map_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить карту", "", "Изображения (*.png *.jpg)")
        if file_path:
            self.map_image = QPixmap(file_path)
            self.image_label.setPixmap(self.map_image)

    def start_creating_polygon(self):
        self.polygon_points = []

    def get_mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            self.polygon_points.append((event.pos().x(), event.pos().y()))
            self.update_image()

    def update_image(self):
        if self.map_image:
            pixmap = self.map_image.copy()
            painter = QPainter(pixmap)
            painter.setPen(QPen(QColor('red'), 2))
            for i in range(len(self.polygon_points) - 1):
                painter.drawLine(self.polygon_points[i][0], self.polygon_points[i][1], self.polygon_points[i+1][0], self.polygon_points[i+1][1])
            painter.end()
            self.image_label.setPixmap(pixmap)

    def add_location(self):
        # Создание локации и добавление ее к базе данных
        location_name = self.location_name_input.text()
        location_description = self.location_description_input.toPlainText()
        location_leads_to = self.location_leads_to_input.text()
        with Session() as session:
            # Добавление в базу данных
            location = Location(name=location_name, description=location_description, leads_to=int(location_leads_to) if location_leads_to else None)
            session.add(location)
            session.commit()

            # Создание MapObjectPolygon
            polygon = MapObjectPolygon(name="Новый полигон", map_id=1, location_id=location.id, poygon_list_json=json.dumps(self.polygon_points))
            session.add(polygon)
            session.commit()