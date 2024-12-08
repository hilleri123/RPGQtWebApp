from widgets.item_widget import ItemWidget
from scheme import *


class LocationGameItemWidget(ItemWidget):
    def __init__(self, item: GameItem, parent=None):
        super().__init__(item=item)

    def on_edit_item(self):
        pass

    def on_delete(self):
        if self.item is not None:
            for w in self.session.query(WhereObject).filter(WhereObject.gameItemId == self.item.id).all():
                self.session.delete(w)
            self.session.commit()
        self.deleted.emit()
