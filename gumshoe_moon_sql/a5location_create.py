
from a4gameitem_create import *


def make_action_for_location(location, action, markConditionJson=None):
    session.add(action)
    session.commit()
    session.add(GameCondition(
        locationId=location.id,
        playerActionId=action.id,
        markConditionJson=markConditionJson
    ))
    session.commit()

Shuttle = Location(name="Челнок", shape=0, offsetX=0, offsetY=0, width=0, height=0, description="""
В челноке команда прибывает на Луну...
""", mapId=moon_station.id)
session.add(Shuttle)
session.commit()
session.add(WhereObject(
    gameItemId=Instruments1.id,
    locationId=Shuttle.id
))

Ravine = Location(name="Овраг", shape=0, offsetX=28, offsetY=28, width=28, height=28, description="""
Взлет отсюда - проверка 4 Вождение.
По пути отсюда ко входу видно склад, у него
будка с роботом(профессионалы могут понять, что это робот для разгона
митингов). Инженеры могут заметить, что к котеджу ведет куча кабелей питания.
Кабели должны были лежать под землей, но их давно покрасили, чтоб пройти проверки,
а сейчас их видно, тк краска осыпается.
""", mapId=moon_station.id)
session.add(Ravine)
session.commit()
make_action_for_location(
    Ravine,
    PlayerAction(
        description="Идти отсюда/сюда. Тащиться от оврага в скафандре то еще упражнение, осбоенно со снарежением.",
        needSkillIdsConditionsJson=makeSkillConditionsJson([Athletics, 4],)
    )
)


Parking = Location(name="Парковка", shape=0, offsetX=68, offsetY=68, width=68, height=68, description="""
Издалека виден указатель, что она платная. Но если подойти
поближе, то видно, что лицензия на сбор за парковку кончилась 10 лет назад.
Абсолютно пустая и рекламы не так много.
""", mapId=moon_station.id)
session.add(Parking)
session.commit()

Checkpoint = Location(name="Проходная", shape=0, offsetX=318, offsetY=318, width=318, height=318, description="""
Есть будка консьержа, работает вентиляция, светильники в норме,
но свет горит только в резервных лампах(свет тусклый). Есть камеры. В будке
консьержа есть телевизоры, на которых изображение с камер проходной и
комнаты ожидания. На стене план здания, переклеенный так, что толщина уже больше 10 см. Из него ничего не понятно. Есть окна.
""", mapId=moon_station.id)
session.add(Checkpoint)
session.commit()

WaitingRoom = Location(name="Комната ожидания", shape=0, offsetX=318, offsetY=318, width=318, height=318, description="""
Окон нет. Есть камера, нет вентиляции, куча пыли, посылки,
коробки и прочий мусор.
""", mapId=moon_station.id)
session.add(WaitingRoom)
session.commit()
session.add(WhereObject(
    gameItemId=Chemicals1.id,
    locationId=Checkpoint.id
))
session.add(WhereObject(
    gameItemId=Chemicals2.id,
    locationId=Checkpoint.id
))
session.commit()


Kitchen1 = Location(name="Кухня 1", shape=0, offsetX=458, offsetY=458, width=458, height=458, description="""
Есть окна и вентиляция. Всякая бытовая утварь. 
""", mapId=moon_station.id)
session.add(Kitchen1)
session.commit()
make_action_for_location(
    Kitchen1,
    PlayerAction(
        description="Из записей можно понять (Анализ текста/Извлечение данных), что Кухня 2 была закрыта месяц назад, тогда же начали делать 11 порций вместо 12.",
        needSkillIdsConditionsJson=makeSkillConditionsJson(TextAnalysis,DataExtraction)
    )
)

Kitchen2 = Location(name="Кухня 2", shape=0, offsetX=670, offsetY=670, width=670, height=670, description="""
Дверь запечатана(внешими конструкциями, которе явно менее
надежны, чем дверь) и закрыта на карантин. Вентиляция есть, окно тоже.
Тут лежат останки(кости) Повар 1, Повар 2, Рабочий, Бухгалтер 2. В холодильнике ледит
труп Менеджер 2. Тут же плодятся ГМО жуки, тут они и живут.
""", mapId=moon_station.id)
session.add(Kitchen2)
session.commit()

Corridor1 = Location(name="Коридор 1", shape=0, offsetX=458, offsetY=458, width=458, height=458, description="""
Вентеляции и окон нет. Гул каких-то механизмов, из-за чего
почти ничего не слышно.
""", mapId=moon_station.id)
session.add(Corridor1)
session.commit()

Corridor2 = Location(name="Коридор 2", shape=0, offsetX=628, offsetY=628, width=628, height=628, description="""
Вентеляции и окон нет. Хорошо слышно, что происходит в Бараки
и Душевые. Стены туда можно проломить.
""", mapId=moon_station.id)
session.add(Corridor2)
session.commit()

LivingArea = Location(name="Жилая часть", shape=0, offsetX=458, offsetY=458, width=458, height=458, description="""
Есть окно, камера, вентиляция. Ездит робот пылесос. Автомат с клешней,
внутри которого сладкая еда. Требуется скорость рекации, обычному человеку
достать ничего не выйдет.
""", mapId=moon_station.id)
session.add(LivingArea)
session.commit()
make_action_for_location(
    LivingArea,
    PlayerAction(
        description="Можно за час разобрать робот пылесос, внутри которого можно найти кровь 2- Охранник 2 и гильзы.",
        needSkillIdsConditionsJson=makeSkillConditionsJson(Mechanics,)
    )
)

Barracks = Location(name="Бараки", shape=0, offsetX=458, offsetY=458, width=458, height=458, description="""
Есть вентиляция и камера. 3 кровати в крови(Повар 1, Повар 2, Рабочий).
""", mapId=moon_station.id)
session.add(Barracks)
session.commit()
session.add(WhereObject(
    gameItemId=Notes.id,
    locationId=Barracks.id
))
session.commit()

Showers = Location(name="Душевые", shape=0, offsetX=698, offsetY=698, width=698, height=698, description="""
Труп капитана охраны с простреленной головой и пистолетом в
руке(Охранник 1).
""", mapId=moon_station.id)
session.add(Showers)
session.commit()
session.add(WhereObject(
    gameItemId=Gun1.id,
    locationId=Showers.id
))
session.commit()

IndustrialZone = Location(name="Пром зона", shape=0, offsetX=848, offsetY=848, width=848, height=848, description="""
Очень много пыли, нет вентиляции и камер. Есть конвеер с кучей
камней. Кровь 4+ на промышленном вентиляторе(продув все зоны) (Механика) Менеджер 1. Кровь 2- в пыли Охранник 2.
""", mapId=moon_station.id)
session.add(IndustrialZone)
session.commit()
session.add(WhereObject(
    gameItemId=Laser.id,
    locationId=IndustrialZone.id
))
session.add(WhereObject(
    gameItemId=Hammer.id,
    locationId=IndustrialZone.id
))
session.add(WhereObject(
    gameItemId=VacuumCleaner.id,
    locationId=IndustrialZone.id
))
session.add(WhereObject(
    gameItemId=Saw.id,
    locationId=IndustrialZone.id
))
session.add(WhereObject(
    gameItemId=Battery0.id,
    locationId=IndustrialZone.id
))
session.add(WhereObject(
    gameItemId=Battery1.id,
    locationId=IndustrialZone.id
))
session.add(WhereObject(
    gameItemId=Instruments2.id,
    locationId=IndustrialZone.id
))
session.commit()

Security = Location(name="Охрана", shape=0, offsetX=848, offsetY=848, width=848, height=848, description="""
Вентиляция есть, окон нет. Погашеные мониторы(без кнопок
включения), видно, что к мониторам из вне идет столько же проводов сколько
камер(6). Компьютер охраны, который может включить мониторы, но требует
авторизации с паролем, админский доступ поможет. Записи с камер на этот
компьютер не сохранялись(все в реальном времени). Пустой ящик с оружием.
Много крови 3+.
""", mapId=moon_station.id)
session.add(Security)
session.commit()
make_action_for_location(
    Security,
    PlayerAction(
        description="Сохранять следующие записи на комп.",
        needSkillIdsConditionsJson=makeSkillConditionsJson(Cryptography,DataExtraction)
    )
)
session.add(WhereObject(
    gameItemId=PlasmaGunClip.id,
    locationId=Security.id
))
session.commit()

ServerRoom = Location(name="Серверная", shape=0, offsetX=848, offsetY=848, width=848, height=848, description="""
Есть вентиляция, окон нет. Кровь 1+ Техник 1. Компьютер, у
которого кнопка включения заклеена бумажкой с надписью "НЕ ТРОГАТЬ,
КТО ТРОНЕТ ТОТ ЛОХ!". Если питание не включено, то с (Механика) можно
запитать компьютер(он включится сам и все будет ок), но тогда навсегда запитается дверь в Реактор(а она заперта изнутри). Через этот компьютер
админ может включить питание всей станции. Взлом админа можно производить
только здесь (проверка 4 Криптография). В компьютере не хватает БП компьютера, поэтому
если он запитан от реактора, то сам он не включится, а если нажать на кнопку
включения, то он загориться и включится пожарная сигнализация, которая
смоет все пятна крови.

Проход в Реактор блокируется замком изнутри, но без питания от реактора
их можно открыть силой(больше силы обычного человека) (5 Ателтика) или спец техникой(например
Лазер).
""", mapId=moon_station.id)
session.add(ServerRoom)
session.commit()
make_action_for_location(
    ServerRoom,
    PlayerAction(
        description="С админским достпуом можно заупстить реактор.",
        changeMarkId=ReactorIsPoweredUp.id,
    ),
    markConditionJson = [AdminPrivilige.id].__repr__()
)
make_action_for_location(
    ServerRoom,
    PlayerAction(
        description="С админским достпуом можно заупстить реактор.",
        changeMarkId=AdminPrivilige.id,
        needSkillIdsConditionsJson=makeSkillConditionsJson([Cryptography,4])
    )
)
session.add(WhereObject(
    gameItemId=ComputerPowerSupply.id,
    locationId=ServerRoom.id
))
session.commit()

Accounting = Location(name="Бухгалтерия", shape=0, offsetX=988, offsetY=988, width=988, height=988, description="""
Вентиляции и окон нет. Один истощенный труп без ран (Бухгалтер 1). При
Бюрократия. понятно, что он умер в ожидании. Куча бумаг, принтеров
и сканеров. С первого взгляда понятно, что тут мощьная система электронного
документооборота.
""", mapId=moon_station.id)
session.add(Accounting)
session.commit()
make_action_for_location(
    Accounting,
    PlayerAction(
        description="2ого апреля можно получить админский доступ с талоном. 4 часа.",
        changeMarkId=AdminPrivilige.id,
        needGameItemIdsJson=[Ticket.id].__repr__()
    )
)
make_action_for_location(
    Accounting,
    PlayerAction(
        description="Открыт неоплачиваемый отпуск для Повар 1.",
        changeMarkId=AdminPrivilige.id,
        needSkillIdsConditionsJson=makeSkillConditionsJson(Bureaucracy,)
    )
)
make_action_for_location(
    Accounting,
    PlayerAction(
        description="Составлялся отчет о смерти Бухгалтера 2, который умер.",
        changeMarkId=AdminPrivilige.id,
        needSkillIdsConditionsJson=makeSkillConditionsJson(Bureaucracy,)
    )
)
session.add(WhereObject(
    gameItemId=Ticket.id,
    locationId=Accounting.id
))
session.commit()

Reactor = Location(name="Реактор", shape=0, offsetX=988, offsetY=988, width=988, height=988, description="""
Вентиляции и окон нет. Труп Техник 1 с огнестрельным ранением.
Переключатель реактора. Система фильтров вентиляции(с Техника 2 ).
""", mapId=moon_station.id)
session.add(Reactor)
session.commit()
make_action_for_location(
    Reactor,
    PlayerAction(
        description="Можно заупстить реактор.",
        changeMarkId=ReactorIsPoweredUp.id,
    )
)
make_action_for_location(
    Reactor,
    PlayerAction(
        description="Можно распылить яд, но все члены команды должны быть в скафандрах.",
        needSkillIdsConditionsJson=makeSkillConditionsJson(Mechanics)
    )
)

Shipping = Location(name="Отгрузка", shape=0, offsetX=1208, offsetY=1208, width=1208, height=1208, description="""
Вентиляции и окон нет, но есть выход наружу. Бензиновый грузовик
с полным баком и малой поломкой(Механика/Вождение). Кровь 2- и труп Охранник 2
с раной от укуса.
""", mapId=moon_station.id)
session.add(Shipping)
session.commit()
make_action_for_location(
    Shipping,
    PlayerAction(
        description="Починить грузовик. 3 часа.",
        needSkillIdsConditionsJson=makeSkillConditionsJson(Mechanics, Driving)
    )
)
session.add(WhereObject(
    gameItemId=PlasmaGun.id,
    locationId=Shipping.id
))
session.commit()

MedicalBay = Location(name="Мед. Отсек", shape=0, offsetX=698, offsetY=698, width=698, height=698, description="""
Кровь 2- Охранник 2. Остались только пустые склянки спирта,
стекловата и пластыри "для пальцев левой ноги".
""", mapId=moon_station.id)
session.add(MedicalBay)
session.commit()
session.add(WhereObject(
    gameItemId=Chemicals3.id,
    locationId=Checkpoint.id
))
session.commit()


WareHouse = Location(name="Склад", shape=0, offsetX=188, offsetY=188, width=188, height=188, description="""
Робот дает пройти только пропускам Техников.
Трупы Охранник 3 и Техник 2. Куча провизии, в основном сладкое. Есть дизельный генератор,
с его помощью можно зарядить батарейки. Есть экзосеклет позволяющий легко носить большие предметы (Механика/Техника/Извлечение данных чтоб настроить его на +2 урон в ближнем бою).
""", mapId=moon_station.id)
session.add(WareHouse)
session.commit()
session.add(WhereObject(
    gameItemId=Plan.id,
    locationId=WareHouse.id
))
session.commit()

SecretRoom = Location(name="Подземная серверная", shape=0, offsetX=0, offsetY=0, width=0, height=0, description="""
Сюда можно попасть, только продыврявив пол в Душевых. Тут можете найти
комнату управления(если есть админ), там посмотреть
все отчеты о перемещениях и пульсе (включая отчет о смерти Менеджер 2).
""", mapId=moon_station.id)
session.add(SecretRoom)
session.commit()
make_action_for_location(
    SecretRoom,
    PlayerAction(
        description="За майинг здесь большая выгода, но выключится резервное питание. При отсутсвии обоих питаний воздуха хватит на 30 минут. Жуки почувствуют это первыми, а игроки через 10 мин.",
        needSkillIdsConditionsJson=makeSkillConditionsJson(Cryptography,)
    )
)


MainARoom = Location(name="Основной зал", shape=0, offsetX=220, offsetY=220, width=220, height=220, description="""
Большой зал заполненный людьми. Вся стена исписана правилами работы аэропорта, поправками к правилам, поправками к поправкам.
Огромная очередь на стойку регистрации. Среди кучи людей выделяется группа вооруженных людей в разной форме, с разным вооружением, 
которые сидят отсраненно. Есть механик, который чинит рекламный стэнд (1 час) в течении первых 2 часов.
""", mapId=airport_map.id)
session.add(MainARoom)
session.commit()
make_action_for_location(
    MainARoom,
    PlayerAction(
        description="Стоять в очереди 5 часов.",
        changeMarkId=ShattleKnowladge.id,
    )
)
make_action_for_location(
    MainARoom,
    PlayerAction(
        description="Взгялнув на очередь и на бумаги, понятно, что надо сразу идти судиться.",
        needSkillIdsConditionsJson=makeSkillConditionsJson(Bureaucracy,)
    )
)
make_action_for_location(
    MainARoom,
    PlayerAction(
        description="прочтить правила пользования (1 час) и понять какие права нарушаются.",
        needSkillIdsConditionsJson=makeSkillConditionsJson(Bureaucracy, DocumentAnalysis, TextAnalysis, Jurisprudence)
    )
)
make_action_for_location(
    MainARoom,
    PlayerAction(
        description="техник, который чинит рекламный щит(средний доход). Можно помочь ему в починке, но надо доказать, что ты сотрудник. Можно хакнуть и крутить рекламу(Криптография). Если помогать, то он будет постоянно говорить про перекур и как он хочет курить. Если помочь, то он может провести в курилку.",
        needSkillIdsConditionsJson=makeSkillConditionsJson(Mechanics,)
    )
)
make_action_for_location(
    MainARoom,
    PlayerAction(
        description="Есть толпа военных налегке к ним можно прибиться, если есть оружие. Послушав их разговоры, можно понять, что их понабрали по объявлениям. Вместе с ними можно пройти на площадку (2 часа). Но потом надо как-то отделиться от группы (Знание языков/Лесть/Бюрократия) или причина."
    )
)

WCARoom = Location(name="Туалет", shape=0, offsetX=180, offsetY=180, width=180, height=180, description="""
Здесь достаточно чисто, на стенах нет никаких надписей, только график уборки туалетов(каждый час).
""", mapId=airport_map.id)
session.add(WCARoom)
session.commit()
make_action_for_location(
    WCARoom,
    PlayerAction(
        description="В тулаете срет в первый час работник аэропорта, у него можно украсть штаны(из штанов) пропуск.",
        needSkillIdsConditionsJson=makeSkillConditionsJson(Thievery,)
    )
)
make_action_for_location(
    WCARoom,
    PlayerAction(
        description="Можно понять, что одна из стен, картонная. Но каждый час ходит уборщица, которая донесет полиции про дырку.",
        needSkillIdsConditionsJson=makeSkillConditionsJson(AppliedPhysics,Architecture,StreetSmarts,Penetration)
    )
)

MedARoom = Location(name="Мед. кабинет", shape=0, offsetX=180, offsetY=180, width=180, height=180, description="""
Если нет причины тут находиться, то выгонят.
В компе мед кабинета можно порыться с Извлечение данных и узнать где шатл в расписании экстренной помощи.
""", mapId=airport_map.id)
session.add(MedARoom)
session.commit()
make_action_for_location(
    MedARoom,
    PlayerAction(
        description="В компе мед кабинета можно порыться и узнать где шатл в расписании экстренной помощи.",
        changeMarkId=ShattleKnowladge.id,
        needSkillIdsConditionsJson=makeSkillConditionsJson(DataExtraction,)
    )
)
session.add(WhereObject(
    gameItemId=Chemicals0.id,
    locationId=MedARoom.id
))
session.commit()

ChangeARoom = Location(name="Раздевалка", shape=0, offsetX=180, offsetY=180, width=180, height=180, description="""
Куча шкафчиков для одежды с разной специализацией(Уборщик, механик, медик, рабочий, грузчик).
""", mapId=airport_map.id)
session.add(ChangeARoom)
session.commit()
make_action_for_location(
    ChangeARoom,
    PlayerAction(
        description="Из шкафчиков можно достать пропуска.",
        needSkillIdsConditionsJson=makeSkillConditionsJson(Thievery,Cryptography,Penetration)
    )
)

PoliceARoom = Location(name="Пропускной пункт", shape=0, offsetX=220, offsetY=220, width=220, height=220, description="""
Человек 10 полицейских, металодетекторы и сканеры есть, но запрещено проносить только свою еду и алкоголь.
""", mapId=airport_map.id)
session.add(PoliceARoom)
session.commit()
make_action_for_location(
    PoliceARoom,
    PlayerAction(
        description="Договориться с полицией на проход, но нужна очень хорошая причина.",
        changeMarkId=ShattleKnowladge.id,
        needSkillIdsConditionsJson=makeSkillConditionsJson(PoliceJargon,)
    )
)

BaggageARoom = Location(name="Склад багажа", shape=0, offsetX=60, offsetY=60, width=60, height=60, description="""
Лента багажа и туда-сюда снуют люди. Добраться до выхода незамеченным - сложная задача.
Правильная одежда дает +2, а просто спец одежда +1. Порядок: багаж, лента, выход.
""", mapId=airport_map.id)
session.add(BaggageARoom)
session.commit()
make_action_for_location(
    BaggageARoom,
    PlayerAction(
        description="Добраться до багажа. Иначе встреча с начальником смены (механик).",
        changeMarkId=ShattleKnowladge.id,
        needSkillIdsConditionsJson=makeSkillConditionsJson([Penetration, 5],)
    )
)
make_action_for_location(
    BaggageARoom,
    PlayerAction(
        description="Перебраться через ленту. Иначе встреча с группой рабочих ленты (рабочий).",
        needSkillIdsConditionsJson=makeSkillConditionsJson([Penetration, 5],)
    )
)
make_action_for_location(
    BaggageARoom,
    PlayerAction(
        description="Добраться до выхода. Иначе встреча с надсмоторщиком над грузчиками (грузчик).",
        changeMarkId=ShattleKnowladge.id,
        needSkillIdsConditionsJson=makeSkillConditionsJson([Penetration, 5],)
    )
)

session.add(WhereObject(
    gameItemId=AssaultRifle.id,
    locationId=BaggageARoom.id
))
session.add(WhereObject(
    gameItemId=Instruments0.id,
    locationId=BaggageARoom.id
))
session.add(WhereObject(
    gameItemId=Gun0.id,
    locationId=BaggageARoom.id
))
session.commit()

CourtARoom = Location(name="Суд", shape=0, offsetX=370, offsetY=370, width=370, height=370, description="""
Суд с присяжными, это пенсионеры за 200, которые пришли сюда за купоном от партнера аэропорта на скидку для замены травоядной челюсти.
""", mapId=airport_map.id)
session.add(CourtARoom)
session.commit()
make_action_for_location(
    CourtARoom,
    PlayerAction(
        description="Суд (2 часа) 2 этапа: сформировать претензию, защить ее(Лесть/Притворсто/Ведение переговоров/...). Знаете где шатл.",
        changeMarkId=ShattleKnowladge.id,
        needSkillIdsConditionsJson=makeSkillConditionsJson(Flattery,Pretending,Negotiation)
    )
)

    