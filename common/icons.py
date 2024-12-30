from PyQt5.QtGui import QIcon
import resources_rc


def get_icon(name: str) -> QIcon:
    return QIcon(f":/icons/{name}.png")

def edit_icon() -> QIcon:
    return get_icon("edit")

def connect_icon() -> QIcon:
    return get_icon("connected")

def lock_icon() -> QIcon:
    return get_icon("lock")

def move_icon() -> QIcon:
    return get_icon("move")

def ok_icon() -> QIcon:
    return get_icon("ok")

def delete_icon() -> QIcon:
    return get_icon("delete")

def location_icon() -> QIcon:
    return get_icon("location")

def lost_icon() -> QIcon:
    return get_icon("lost")

def npc_icon() -> QIcon:
    return get_icon("npc")

def player_icon() -> QIcon:
    return get_icon("player")

def add_icon() -> QIcon:
    return get_icon("add")

def error_icon() -> QIcon:
    return lost_icon()

def all_players() -> QIcon:
    return get_icon("all_players")

def select_players() -> QIcon:
    return get_icon("select_players")
