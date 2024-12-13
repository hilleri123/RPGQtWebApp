import re
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QPushButton, QWidget, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from .autoresize import AutoResizingTextEdit


class HtmlTextEdit(AutoResizingTextEdit):
    def __init__(self, add_font_size=4, is_fixed=False, max_height=None, parent=None):
        self.add_font_size = add_font_size
        super().__init__(max_height=max_height, is_fixed=is_fixed, parent=parent)

    def toHtml(self):
        html_content = super().toHtml()

        # Увеличиваем размер шрифта в HTML (например, на 4pt)
        updated_html = re.sub(
            r"font-size:(\d+)pt;",
            lambda match: f"font-size:{int(match.group(1)) + self.add_font_size}pt;",
            html_content,
        )
        return updated_html

    def setHtml(self, html_content):
        if html_content is None:
            return
        updated_html = re.sub(
            r"font-size:(\d+)pt;",
            lambda match: f"font-size:{int(match.group(1)) - self.add_font_size}pt;",
            html_content,
        )
        res = super().setHtml(updated_html)
        self.auto_resize()
        return res
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_B and event.modifiers() == Qt.ControlModifier:
            self.toggle_bold()
        else:
            super().keyPressEvent(event)

    def toggle_bold(self):
        cursor = self.textCursor()  # Получаем текущий курсор
        if not cursor.hasSelection():
            return  # Если нет выделенного текста, ничего не делаем

        # Получаем текущий формат текста
        current_format = cursor.charFormat()
        
        # Переключаем жирность текста
        if current_format.fontWeight() == QFont.Bold:
            current_format.setFontWeight(QFont.Normal)  # Убираем жирный шрифт
        else:
            current_format.setFontWeight(QFont.Bold)  # Устанавливаем жирный шрифт

        # Применяем формат к выделенному тексту
        cursor.mergeCharFormat(current_format)

    