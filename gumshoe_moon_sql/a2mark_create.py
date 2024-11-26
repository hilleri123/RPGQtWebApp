
from a1playablecharacter_create import *

ShattleKnowladge = Mark(name="Номер шатла", description="Знают, номер нужного шатла", isActivated=False, status=-1)
session.add(ShattleKnowladge)

ReactorIsPoweredUp = Mark(name="Реактор запущен", description="Двери открываются сразу, включается свет, может сработать система пожаротушения", isActivated=False, status=-1)
session.add(ReactorIsPoweredUp)

AdminPrivilige = Mark(name="Админский доступ", description="Получен доступ админа", isActivated=False, status=-1)
session.add(AdminPrivilige)

session.commit()