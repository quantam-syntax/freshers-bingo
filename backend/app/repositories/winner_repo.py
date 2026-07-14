from app.extensions import db
from app.models.winner import Winner
from app.models.bingo import BingoCard
from sqlalchemy.orm import joinedload


def get_all():
    return Winner.query.options(
        joinedload(Winner.fresher),
        joinedload(Winner.bingo_card).joinedload(BingoCard.cells)
    ).order_by(Winner.rank).all()


def count():
    return Winner.query.count()


def add_winner(fresher_id, bingo_card_id):
    # Lock winners table to prevent race conditions when checking count and assigning rank
    db.session.execute(db.text("LOCK TABLE winners IN EXCLUSIVE MODE"))
    current_count = count()
    if current_count >= 20:
        return None
    winner = Winner(
        fresher_id=fresher_id,
        bingo_card_id=bingo_card_id,
        rank=current_count + 1,
    )
    db.session.add(winner)
    db.session.commit()
    return winner


def is_winner(fresher_id):
    return Winner.query.filter_by(fresher_id=fresher_id).first() is not None
