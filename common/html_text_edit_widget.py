import re
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QPushButton, QWidget, QFileDialog
from .autoresize import AutoResizingTextEdit


class HtmlTextEdit(AutoResizingTextEdit):
    def __init__(self):
        super().__init__()

    def toHtml(self, add_font_size=4):
        html_content = self.toHtml()

        # Увеличиваем размер шрифта в HTML (например, на 4pt)
        updated_html = re.sub(
            r"font-size:(\d+)pt;",
            lambda match: f"font-size:{int(match.group(1)) + add_font_size}pt;",
            html_content,
        )
        return updated_html


    