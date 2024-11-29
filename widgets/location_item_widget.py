from widgets.item_widget import ItemWidget
from scheme import *


class LocationGameItemWidget(ItemWidget):
    def __init__(self, item: GameItem, parent=None):
        super().__init__(item=item)

    def on_edit_item(self):
        pass

    def on_delete(self):
        print("Create me!")
