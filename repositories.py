from scheme import *
import json


def check_marks_in_condition(condition_list: list[GameCondition]) -> list[GameCondition]:
    session = Session()
    res = []
    for condition in condition_list:
        if condition.markConditionJson is None:
            res.append(condition)
            continue
        mark_json = json.loads(condition.markConditionJson)
        if "activated" in mark_json:
            activated = session.query(Mark).filter(
                Mark.id.in_(mark_json["activated"]),
                Mark.isActivated == True
            ).all()
            if len(activated) > 0:
                res.append(condition)
                continue

        res.append(condition)
        # TODO status
    return res


def reset_scenario():
    session = Session()
    first_record = session.query(GlobalMap).first()

    if first_record:
        first_start_time = first_record.start_time
        if first_start_time:
            session.query(GlobalMap).update({GlobalMap.time: first_start_time})
            session.commit()

    session.query(Location).filter(Location.is_shown == 1).update({Location.is_shown: 0})
    session.commit()

    session.query(Note).update({Note.player_shown_json: '[]'})
    session.commit()

    session.query(SceneMap).filter(SceneMap.is_shown == 1).update({SceneMap.is_shown: 0})
    session.commit()

    session.query(MapObjectPolygon).filter(MapObjectPolygon.is_shown == 1).update({MapObjectPolygon.is_shown: 0})
    session.commit()

    session.query(PlayerCharacter).update({
        PlayerCharacter.map_id: None, 
        PlayerCharacter.location_id: None, 
        PlayerCharacter.address: None, 
        PlayerCharacter.player_locked: None,
        PlayerCharacter.time: None,
        })
    session.commit()
    
    session.query(Stat).update({Stat.value: Stat.initValue})
    session.commit()

    session.query(GameEvent).update({GameEvent.happend: False})
    session.commit()

