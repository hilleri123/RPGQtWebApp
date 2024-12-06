import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from scheme import *
from PyQt5.QtCore import QThread, QObject
from web_app.flask_main import (
    app, 
    broadcast_reload, broadcast_notes_reload, broadcast_character_reload, broadcast_map_reload, 
    set_callbacks)

class FlaskThread(QThread):
    def __init__(self, flask_app):
        super().__init__()
        self.flask_app = flask_app

    def run(self):
        self.flask_app.run(host='0.0.0.0', port=2666)

    def reload(self):
        broadcast_reload()
        
    def reload_character(self):
        broadcast_character_reload()
        
    def reload_map(self):
        broadcast_map_reload()
        
    def reload_notes(self):
        broadcast_notes_reload()

if __name__ == "__main__":
    flask_thread = FlaskThread(app)
    flask_thread.start()

    app = QApplication(sys.argv)
    m = MainWindow()
    set_callbacks(
        callback_map=m.update_map,
        callback_item=m.update_character_item,
        callback_char_stat=m.update_character_stat,
        callback_connection=m.update_connections
        )
    m.need_to_reload.connect(flask_thread.reload)
    m.characters_updated.connect(flask_thread.reload_character)
    m.map_image_saved.connect(flask_thread.reload_map)
    m.notes_updated.connect(flask_thread.reload_notes)
    m.show()
    sys.exit(app.exec_())