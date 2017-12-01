import json

from database import get_session
from database import PlayersItemsTable, LevelsTable, ItemsTable


def get_level(level_id):
    session = get_session()

    return session.query(LevelsTable).filter_by(id=level_id).one()


def get_items(level_id):
    session = get_session()

    items = session.query(ItemsTable).filter_by(level_id=level_id).all()
    players_items = session.query(PlayersItemsTable).filter_by(level_id=level_id).all()

    data = {
        'open': [],
        'complete': []
    }
    for item in items:
        answer = json.loads(item.answer)
        data['open'].append({
            "id": item.id,
            "item_type": item.item_type,
            "question": item.question,
            "bonus": True if answer['bonus'] else False
        })

    for item in players_items:
        data['complete'].append({
            "id": item.item_id,
            "item_type": item.item.item_type,
            "question": item.item.question,
            "solved": item.player.name
        })

    return data
