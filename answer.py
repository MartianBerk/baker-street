import json

from database import get_session
from database import ItemsTable, PlayersItemsTable


def check(item_id, player_answer, player_id):
    session = get_session()
    item = session.query(ItemsTable).filter_by(id=item_id).one()
    answer = json.loads(item.answer)

    # Check question not already answered
    if session.query(PlayersItemsTable).filter_by(item_id=item_id).all():
        return {'correct': False, 'bonus': False, 'message': 'Already answered.'}

    player_answer_parts = player_answer.lower().split(',')
    player_answer_parts = [x for x in player_answer.lower().split(' ')]

    # Check answer
    correct = False
    if answer['type'] == 'is':
        if answer['answer'] == player_answer.lower():
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

    return {'correct': correct, 'bonus': bonus}
