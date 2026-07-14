from app.extensions import db
from app.models.bingo import BingoCard, BingoCell
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))


def find_by_fresher_id(fresher_id):
    return BingoCard.query.filter_by(fresher_id=fresher_id).first()


def create_card(fresher_id, letters):
    card = BingoCard(fresher_id=fresher_id)
    db.session.add(card)
    db.session.flush()
    for i, letter in enumerate(letters):
        cell = BingoCell(bingo_card_id=card.id, position=i, letter=letter)
        db.session.add(cell)
    db.session.flush()
    return card


def find_cell_by_id(cell_id):
    return BingoCell.query.get(cell_id)


def update_cell_photo(cell, photo_url):
    cell.photo_url = photo_url
    cell.filled_at = datetime.now(IST)
    db.session.commit()
    return cell


def mark_card_completed(card):
    card.completed_at = datetime.now(IST)
    db.session.commit()
    return card


def count_completed():
    return BingoCard.query.filter(BingoCard.completed_at.isnot(None)).count()
