from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox, QGridLayout, QListWidget, QListWidgetItem, QCheckBox, QSpinBox, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QColor, QMouseEvent, QIcon
from PyQt5.QtCore import pyqtSignal
from scheme import *
from .autoresize import AutoResizingListWidget
from .icons import add_icon, delete_icon, edit_icon



class ElementWidget(QWidget):
    def __init__(self, element_id, element_cls, dialog_cls):
        super().__init__()

        self.element_id = element_id
        self.element_cls = element_cls
        self.dialog_cls = dialog_cls

        layout = QHBoxLayout()
        self.setLayout(layout)

        try:
            with Session() as session:
                element = session.query(self.element_cls).get(self.element_id)
                layout.addWidget(QLabel(element.name))
        except:
            pass

        edit_button = QPushButton(edit_icon(), None)
        edit_button.clicked.connect(self.edit_element)
        layout.addWidget(edit_button)

        delete_button = QPushButton(delete_icon(), None)
        delete_button.clicked.connect(self.delete_element)
        layout.addWidget(delete_button)

    def edit_element(self):
        dialog = self.dialog_cls(self.element_id)
        dialog.exec_()

    def delete_element(self):
        with Session() as session:
            element = session.query(self.element_cls).get(self.element_id)
            if element:
                session.delete(element)
                session.commit()
                self.parent().update_elements()


class TableWidget(QWidget):
    def __init__(self, element_cls, dialog_cls):
        super().__init__()

        self.element_cls = element_cls
        self.dialog_cls = dialog_cls

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.elements_layout = QVBoxLayout()
        layout.addLayout(self.elements_layout)

        self.add_button = QPushButton(add_icon(), None)
        self.add_button.clicked.connect(self.add_element)
        layout.addWidget(self.add_button)

        self.update_elements()

    def update_elements(self):
        while self.elements_layout.count():
            child = self.elements_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        with Session() as session:
            for element in session.query(self.element_cls).all():
                widget = ElementWidget(element.id, self.element_cls, self.dialog_cls)
                self.elements_layout.addWidget(widget)

    def add_element(self):
        with Session() as session:
            new_element = self.element_cls(name="Новый элемент")
            session.add(new_element)
            session.commit()
            self.update_elements()
