import json

from database import get_session
from database import ItemsTable, PlayersItemsTable


def check(item_id, player_answer, player_id):
    session = get_session()
    item = session.query(ItemsTable).filter_by(id=item_id).one()
    answer = json.loads(item.answer)

    player_answer_parts = player_answer.lower().split(',')
    player_answer_parts = [x for x in player_answer.lower().split(' ')]

    # Check answer
    correct = False
    if answer['type'] == 'is':
        if answer['answer'] in player_answer_parts:
            correct = True
    elif answer['type'] == 'all':
        if all(x in player_answer_parts for x in answer['answer']):
            correct = True

    # Check bonus
    bonus = False
    if correct and answer['bonus']:
        if answer['bonus']['type'] == 'either':
            for part in player_answer_parts:
                if part in answer['bonus']['answer']:
                    bonus = True
        elif answer['bonus']['type'] == 'order':
            if player_answer_parts == answer['bouns']['answer']:
                bonus = True

    if correct:
        player_item = PlayersItemsTable(
            player_id=player_id,
            item_id=item_id,
            level_id=item.level_id,
            bonus=('T' if bonus else 'F')
        )
        session.add(player_item)
        session.commit()

        return True
    else:
        return False
