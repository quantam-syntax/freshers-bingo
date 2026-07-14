from app.extensions import db
from app.models.challenge import Challenge, ChallengePick
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))


def get_all():
    return Challenge.query.order_by(Challenge.id).all()


def get_unused():
    return Challenge.query.filter_by(is_used=False).all()


def get_used_count():
    return Challenge.query.filter_by(is_used=True).count()


def find_by_id(challenge_id):
    return Challenge.query.get(challenge_id)


def create(text, admin_id):
    challenge = Challenge(text=text, created_by_admin_id=admin_id)
    db.session.add(challenge)
    db.session.commit()
    return challenge


def update(challenge, text):
    challenge.text = text
    db.session.commit()
    return challenge


def delete(challenge):
    db.session.delete(challenge)
    db.session.commit()


def mark_used(challenge):
    challenge.is_used = True
    challenge.used_at = datetime.now(IST)
    db.session.flush()
    pick = ChallengePick(challenge_id=challenge.id)
    db.session.add(pick)
    db.session.commit()
    return challenge


def mark_unused(challenge):
    challenge.is_used = False
    challenge.used_at = None
    db.session.commit()
    return challenge
