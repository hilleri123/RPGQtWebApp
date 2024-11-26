
from a3scenemap_create import *

Instruments0 = GameItem(name="Инструменты", text="Набор инструментов включает гаечные ключи, отвертки, молоток и другие необходимые предметы.")
session.add(Instruments0) #
Instruments1 = GameItem(name="Инструменты", text="Набор инструментов включает гаечные ключи, отвертки, молоток и другие необходимые предметы.")
session.add(Instruments1) #
Instruments2 = GameItem(name="Инструменты", text="Набор инструментов включает гаечные ключи, отвертки, молоток и другие необходимые предметы.")
session.add(Instruments2) #
Chemicals0 = GameItem(name="Химикаты", text="Используются для производства еды из пластика")
session.add(Chemicals0) #
Chemicals1 = GameItem(name="Химикаты", text="Используются для производства еды из пластика")
session.add(Chemicals1) #
Chemicals2 = GameItem(name="Химикаты", text="Используются для производства еды из пластика")
session.add(Chemicals2) #
Chemicals3 = GameItem(name="Химикаты", text="Используются для производства еды из пластика")
session.add(Chemicals3) #
Notes = GameItem(name="Дневник", text="Из дневника можно понять, что каждую пятницу в 21:00 в Пром зона запускается выдув в космос пыли и прочего. Что Повар 1 и Повар 2 начинают смену на час раньше остальных и заканчивают на час позже")
session.add(Notes) #
Gun0 = GameItem(name="Пистолет", text="Патроны автоматически пресуются из пыли, но после выстрела формируются гильзы(для антуража). Урон +0.")
session.add(Gun0) #
Gun1 = GameItem(name="Пистолет", text="Патроны автоматически пресуются из пыли, но после выстрела формируются гильзы(для антуража). Урон +0.")
session.add(Gun1) #
Battery0 = GameItem(name="Батарейка", text="Держит заряд долго, но мощности достаточно не для всех устройств.")
session.add(Battery0) #
Battery1 = GameItem(name="Батарейка", text="Держит заряд долго, но мощности достаточно не для всех устройств.")
session.add(Battery1) #
PlasmaGunClip = GameItem(name="Обойма от плазмагана", text="Ооочень старая обойма. Теперь ее нельзя использовать в Плазмагане, без починки.")
session.add(PlasmaGunClip) #
ComputerPowerSupply = GameItem(name="БП компьютера", text="Многофункциональный модуль питания последнего покаления.")
session.add(ComputerPowerSupply) #
PlasmaGun = GameItem(name="Плазмаган", text="Старый, надежный, военный плазмаган с надписью: не прикуривать. Тяжелый. Урон +3.")
session.add(PlasmaGun) #
Ticket = GameItem(name="Талон", text="""
На вторые сутки позволяет получить
админский доступ. Чтоб воспользоваться нужно Бюрократия
Описание: Талон в очередь на получение админских прав с пометкой о
прохождении мед. комиссии, экспертной комиссии, теста на наличие интеллекта
2 степени на имя Пьер Жук 1970 года рождения.
""")
session.add(Ticket) #
Laser = GameItem(name="Лазер", text="Лазер, который старше этой станции. Очень тяжелый, носится вдвоем. Урон +6.")
session.add(Laser) #
VacuumCleaner = GameItem(name="Пылесос", text="Промышленный пылесос, с функцией вдува/выдува. Можно распылять, что-то. Техника + инструменты = Огнемет(Урон +2 против жуков)")
session.add(VacuumCleaner) #
Hammer = GameItem(name="Молоток", text="Пневмо молоток для дробления камня. Тяжелый. Урон 4.")
session.add(Hammer) #
Saw = GameItem(name="Пила", text="Пила по металлу, умная остановка при распиливании органики. Тяжелый. Урон 3/6 против Робот.")
session.add(Saw) #
Plan = GameItem(name="Проектировочный план", text="Из плана понятно, где находится гланая серверная (под душевыми).")
session.add(Plan) #
AssaultRifle = GameItem(name="Модифицированный АК-47", text="Стреляет до 3 очередями (-1 к попаданию). Урон +1.")
session.add(AssaultRifle) #

session.commit()
