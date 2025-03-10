import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QListView, QColorDialog, QCheckBox, QLabel, QSpinBox
)
from PyQt5.QtCore import pyqtSignal, Qt, QModelIndex, QAbstractListModel
from PyQt5.QtGui import QColor
from scheme import *
import json


# Модель для списка точек
class PointsModel(QAbstractListModel):
    def __init__(self, polygon_id):
        super().__init__()
        self.session = Session()
        self.polygon = self.session.query(MapObjectPolygon).get(polygon_id)
        self.points = []  # Список точек (x, y)
        if self.polygon:
            self.points = json.loads(self.polygon.poygon_list_json)

    def rowCount(self, parent=QModelIndex()):
        return len(self.points)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.points):
            return None

        point = self.points[index.row()]
        if role == Qt.DisplayRole:
            return f"Point ({point['x']}, {point['y']})"
        elif role == Qt.DecorationRole:
            return point['color']  # Цвет точки

        return None

    def add_point(self, x, y, color=QColor("black")):
        self.beginInsertRows(QModelIndex(), len(self.points), len(self.points))
        self.points.append({"x": x, "y": y, "color": color})
        self.endInsertRows()

    def remove_point(self, row):
        if 0 <= row < len(self.points):
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.points[row]
            self.endRemoveRows()

    def on_save(self):
        if self.polygon is None:
            return
        self.polygon.poygon_list_json = self.points.__repr__()
        self.session.commit()

# Диалоговое окно
class PolygonDialog(QDialog):
    polygon_selected = pyqtSignal(int)
    polygon_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Points Manager")

        # Основной макет
        layout = QVBoxLayout()

        # Модель и вид списка
        self.model = PointsModel(polygon_id=1) #???
        self.list_view = QListView()
        self.list_view.setModel(self.model)
        layout.addWidget(self.list_view)

        # Поля для добавления точки
        input_layout = QHBoxLayout()
        self.x_input = QSpinBox()
        self.x_input.setMaximum(4000)
        self.y_input = QSpinBox()
        self.y_input.setMaximum(4000)
        input_layout.addWidget(QLabel("X:"))
        input_layout.addWidget(self.x_input)
        input_layout.addWidget(QLabel("Y:"))
        input_layout.addWidget(self.y_input)

        layout.addLayout(input_layout)

        # Кнопка выбора цвета
        color_layout = QHBoxLayout()
        self.color_label = QLabel("Цвет: ")
        self.color_button = QPushButton("Выбрать цвет")
        self.color_button.clicked.connect(self.choose_color)
        color_layout.addWidget(self.color_label)
        color_layout.addWidget(self.color_button)

        layout.addLayout(color_layout)

        # Чекбокс
        self.checkbox = QCheckBox("Активировать функцию")
        layout.addWidget(self.checkbox)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        add_button = QPushButton("Добавить точку")
        add_button.clicked.connect(self.add_point)
        
        remove_button = QPushButton("Удалить выбранную точку")
        remove_button.clicked.connect(self.remove_selected_point)
        
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(remove_button)

        layout.addLayout(buttons_layout)

        # Установка основного макета
        self.setLayout(layout)

    def choose_color(self):
        """Открыть диалог выбора цвета."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.color_label.setText(f"Цвет: {color.name()}")
            self.color_label.setStyleSheet(f"color: {color.name()};")
    
    def add_point(self):
        """Добавить новую точку в список."""
        try:
            x = int(self.x_input.text())
            y = int(self.y_input.text())
            color = self.selected_color if hasattr(self, "selected_color") else QColor("black")
            self.model.add_point(x, y, color)

            # Очистить поля ввода после добавления точки
            self.x_input.clear()
            self.y_input.clear()
        except ValueError:
            print("Введите корректные координаты (целые числа).")

    def remove_selected_point(self):
        """Удалить выбранную точку из списка."""
        selected_indexes = self.list_view.selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            self.model.remove_point(row)
        else:
            print("Выберите точку для удаления.")


            
            
            
        
        
        
        