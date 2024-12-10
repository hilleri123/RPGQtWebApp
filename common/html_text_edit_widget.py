import re
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QPushButton, QWidget, QFileDialog
from .autoresize import AutoResizingTextEdit


class HtmlTextEdit(AutoResizingTextEdit):
    def __init__(self, add_font_size=4, max_height=None, parent=None):
        self.add_font_size = add_font_size
        super().__init__(max_height=max_height, parent=parent)

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
        return super().setHtml(updated_html)

    