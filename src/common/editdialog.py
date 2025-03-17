import sys
from PyQt5.QtWidgets import QSpinBox, QCheckBox, QDialog, QFormLayout, QLabel, QLineEdit, QPushButton
from sqlalchemy import inspect
from scheme import *

class ModelEditor(QDialog):
    def __init__(self, model_instance):
        super().__init__()
        self.model_instance = model_instance
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        
        # Динамически добавляем поля на основе атрибутов класса
        for column in inspect(model_instance.__class__).column_attrs:
            field_name = column.key
            field_value = getattr(model_instance, field_name)
            
            if isinstance(field_value, int):
                field_widget = QSpinBox()
                field_widget.setValue(field_value)
            elif isinstance(field_value, bool):
                field_widget = QCheckBox()
                field_widget.setChecked(field_value)
            elif isinstance(field_value, str):
                field_widget = QLineEdit(field_value)
            else:
                field_widget = QLineEdit(str(field_value))
            self.layout.addRow(QLabel(field_name), field_widget)
        
        # Кнопка для сохранения изменений
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(save_button)
    
    def save_changes(self):
        # Обновляем атрибуты экземпляра класса
        for i in range(self.layout.count()):
            layout_item = self.layout.itemAt(i)
            if layout_item.widget() and isinstance(layout_item.widget(), QLineEdit):
                field_name = layout_item.label().text()
                field_value = layout_item.widget().text()
                setattr(self.model_instance, field_name, field_value)
        
        # Сохраняем изменения в базе данных
        with Session() as session:
            session.add(self.model_instance)
            session.commit()
            session.close()
