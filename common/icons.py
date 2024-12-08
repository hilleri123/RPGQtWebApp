from PyQt5.QtGui import QIcon
import resources_rc


def get_icon(name):
    return QIcon(f":/icons/{name}.png")

def edit_icon():
    return get_icon("edit")

def move_icon():
    return get_icon("move")
