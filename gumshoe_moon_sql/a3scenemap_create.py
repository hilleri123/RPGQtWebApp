
from a2mark_create import *

airport_map = SceneMap(name='Аэропорт', filePath='../data/airport.png', isCurrent=True)
moon_station = SceneMap(name='Лунная станция', filePath='../data/moon_map.png', isCurrent=False)

session.add(airport_map)
session.add(moon_station)

session.commit()