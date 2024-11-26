from PyQt5.QtCore import QRect


class Location:
    curr_id = 0

    def __init__(self, name="", description="", rect=QRect):
        self.id = Location.curr_id
        Location.curr_id += 1
        self.name = name
        self.description = description
        self.rect = rect


test_locs = [Location("a", "a"*20, QRect(10,10,20,20)), Location("b", "b"*20, QRect(100,10,20,20))]

def get_location_list():
    return test_locs

def get_location_by_id(location_id: int):
    for l in test_locs:
        if l.id == location_id:
            return l