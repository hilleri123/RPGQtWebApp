from widgets.item_widget import ItemWidget
from scheme import *


class LocationGameItemWidget(ItemWidget):
    def __init__(self, item: GameItem, parent=None):
        super().__init__(db_object=item, parent=parent)
        self.xml_text.setReadOnly(True)

    def on_edit_item(self):
        pass

    def on_delete(self):
        if self.db_object is not None:
            for w in self.session.query(WhereObject).filter(WhereObject.gameItemId == self.db_object.id).all():
                self.session.delete(w)
            self.session.commit()
        self.deleted.emit()
