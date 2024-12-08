from PyQt5.QtGui import QIcon
import resources_rc


def get_icon(name: str) -> QIcon:
    return QIcon(f":/icons/{name}.png")

def edit_icon() -> QIcon:
    return get_icon("edit")

def move_icon() -> QIcon:
    return get_icon("move")
