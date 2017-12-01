from database import get_session
from database import PlayersTable, PlayersItemsTable, ItemsTable
from sqlalchemy import and_

totals = {
    "level_one": 5,
    "level_two": 5,
    "level_three": 5
}


def get_player(player, code):
    # Validate player
    session = get_session()

    try:
        player = session.query(PlayersTable).filter(and_(
            PlayersTable.name == player, PlayersTable.code == code
        )).one()

        return player
    except Exception:
        return False


def level_one_stats(player_id):
    session = get_session()

    items = session.query(ItemsTable).filter_by(level_id=1).all()
    player_items = session.query(PlayersItemsTable).filter(and_(
        PlayersItemsTable.player_id == player_id, PlayersItemsTable.level_id == 1
    )).all()

    data = {
        'complete': [],
        'incomplete': [],
        'solved': 0,
        'total': totals['level_one']
    }

    data['complete'].extend([item.id for item in items if item.status == 'complete'])
    data['incomplete'].extend([item.id for item in items if item.status != 'complete'])

    for item in player_items:
        data['solved'] += 1

    return data


def level_two_stats(player_id):
    session = get_session()

    items = session.query(ItemsTable).filter_by(level_id=2).all()
    player_items = session.query(PlayersItemsTable).filter(and_(
        PlayersItemsTable.player_id == player_id, PlayersItemsTable.level_id == 2
    )).all()

    data = {
        'complete': [],
        'incomplete': [],
        'solved': 0,
        'total': totals['level_two']
    }

    data['complete'].extend([item.name for item in items if item.status == 'complete'])
    data['incomplete'].extend([item.name for item in items if item.staus != 'complete'])

    for item in player_items:
        data['solved'] += 1

    return data


def level_three_stats(player_id):
    session = get_session()

    items = session.query(ItemsTable).filter_by(level_id=3).all()
    player_items = session.query(PlayersItemsTable).filter(and_(
        PlayersItemsTable.player_id == player_id, PlayersItemsTable.level_id == 3
    )).all()

    data = {
        'complete': [],
        'incomplete': [],
        'solved': 0,
        'total': totals['level_three']
    }

    data['complete'].extend([item.name for item in items if item.status == 'complete'])
    data['incomplete'].extend([item.name for item in items if item.staus != 'complete'])

    for item in player_items:
        data['solved'] += 1

    return data
