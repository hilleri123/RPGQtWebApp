
from a5location_create import *


MilitaryComander = NPC(name="Командир подразделения", descriptionText="Сержант, орет матом.", isDead=False)
session.add(MilitaryComander)


session.commit()

MilitaryComanderDialog0 = PlayerAction(
    description="Слинять из строя", 
    needSkillIdsConditionsJson=makeSkillConditionsJson(LanguageKnowledge), 
    )
session.add(MilitaryComanderDialog0)

session.commit()

session.add(GameCondition(
    playerActionId=MilitaryComanderDialog0.id,
    npcId=MilitaryComander.id,
))
session.add(GameCondition(
    locationId=MainARoom.id,
    npcId=MilitaryComander.id,
    text="Стоит и кричит на солдата из-за того, что тот решил открыть консерву пистолетом."
))


session.commit()