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
