from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton
from scheme import *


class LogWidget(QListWidget):
    def __init__(self):
        super().__init__()

    def add_item(self, text: str):
        if self.check_if_last_item_visible():
            scroll_to_bottom = True
        else:
            scroll_to_bottom = False
        self.addItem(text)
        QApplication.processEvents()
        if scroll_to_bottom:
            self.scrollToBottom()

    def log_stat_change(self, character_id: int, stats: dict[int, int]):
        self.session = Session()
        character = self.session.query(PlayerCharacter).get(character_id)
        if character is None:
            self.add_item(f'Character with id={character_id} not found')
            return
        for skill_id, prev_value in stats.items():
            stat = self.session.query(Stat)\
                .filter(Stat.characterId == character_id)\
                .filter(Stat.skillId == skill_id).first()
            if stat is None:
                self.add_item(f'Character ({character.name}) has no skill id={skill_id}')
                continue
            skill = self.session.query(Skill).get(skill_id)
            if skill is None:
                self.add_item(f'Skill with id={skill_id} not found')
                continue
            self.add_item(f'{character.name} {skill.name}: {prev_value} -> {stat.value}')

    def check_if_last_item_visible(self):
        count = self.count()
        if count == 0:
            return False  # В списке нет элементов

        last_item = self.item(count - 1)
        
        return self.visualItemRect(last_item).top() <= self.viewport().height()

    def log_move_item(self, from_player, to_player, to_location_id):
        # TODO
        self.add_item(f'{from_player} -> {to_player} {to_location_id}')
