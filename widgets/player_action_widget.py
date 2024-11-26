from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QComboBox, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal


class PlayerActionWidget(QWidget):
    # Сигнал для уведомления об изменении данных
    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Поля для редактирования
        self.id_field = QLabel()  # Поле для отображения ID (только для чтения)
        self.description_field = QTextEdit()
        self.need_skill_ids_field = QTextEdit()
        self.change_mark_field = QComboBox()
        self.get_game_item_field = QComboBox()
        self.need_game_item_ids_field = QTextEdit()

        # Кнопка сохранения
        self.edit_button = QPushButton()
        self.edit_button.setIcon(QIcon.fromTheme("preferences-system"))

        # Основной макет
        layout = QVBoxLayout(self)
        
        # Формы для полей
        form_layout = QFormLayout()
        form_layout.addRow("ID:", self.id_field)
        form_layout.addRow("Описание:", self.description_field)
        form_layout.addRow("Требуемые навыки (JSON):", self.need_skill_ids_field)
        form_layout.addRow("Изменить метку:", self.change_mark_field)
        form_layout.addRow("Получить предмет:", self.get_game_item_field)
        form_layout.addRow("Требуемые предметы (JSON):", self.need_game_item_ids_field)

        layout.addLayout(form_layout)
        
        # Кнопка сохранения
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def set_data(self, player_action, marks=None, game_items=None):
        """
        Устанавливает данные в виджет.
        
        :param player_action: Объект PlayerAction для отображения/редактирования.
        :param marks: Список доступных меток (Mark), если нужно.
        :param game_items: Список доступных игровых предметов (GameItem), если нужно.
        """
        # Устанавливаем данные в поля
        self.id_field.setText(str(player_action.id))
        self.description_field.setPlainText(player_action.description or "")
        self.need_skill_ids_field.setPlainText(player_action.needSkillIdsConditionsJson or "")
        
        # Заполняем выпадающий список меток
        if marks:
            self.change_mark_field.clear()
            for mark in marks:
                self.change_mark_field.addItem(mark.name, mark.id)
            if player_action.changeMarkId is not None:
                index = self.change_mark_field.findData(player_action.changeMarkId)
                if index != -1:
                    self.change_mark_field.setCurrentIndex(index)

        # Заполняем выпадающий список игровых предметов
        if game_items:
            self.get_game_item_field.clear()
            for item in game_items:
                self.get_game_item_field.addItem(item.name, item.id)
            if player_action.getGameItemId is not None:
                index = self.get_game_item_field.findData(player_action.getGameItemId)
                if index != -1:
                    self.get_game_item_field.setCurrentIndex(index)

        self.need_game_item_ids_field.setPlainText(player_action.needGameItemIdsJson or "")

    def save_data(self):
        """
        Сохраняет изменения в объект PlayerAction и отправляет сигнал.
        
        :return: Обновленный объект PlayerAction.
        """
        # Получаем данные из полей
        description = self.description_field.toPlainText()
        need_skill_ids_json = self.need_skill_ids_field.toPlainText()
        
        change_mark_id = (
            self.change_mark_field.currentData() 
            if self.change_mark_field.currentIndex() != -1 
            else None
        )
        
        get_game_item_id = (
            self.get_game_item_field.currentData() 
            if self.get_game_item_field.currentIndex() != -1 
            else None
        )
        
        need_game_item_ids_json = self.need_game_item_ids_field.toPlainText()

        print("Сохраненные данные:")
        print(f"Описание: {description}")
        print(f"Требуемые навыки (JSON): {need_skill_ids_json}")
        print(f"Изменить метку ID: {change_mark_id}")
        print(f"Получить предмет ID: {get_game_item_id}")
        print(f"Требуемые предметы (JSON): {need_game_item_ids_json}")

        # Отправляем сигнал о том, что данные были изменены
        self.dataChanged.emit()
