from app.extensions import db
from app.models.fresher import Fresher


def find_by_roll_no(roll_no):
    return Fresher.query.filter_by(roll_no=roll_no).first()


def find_by_id(fresher_id):
    return Fresher.query.get(fresher_id)


def create(roll_no, name, socials=None):
    fresher = Fresher(roll_no=roll_no, name=name, socials=socials)
    db.session.add(fresher)
    db.session.flush()
    return fresher


def count_all():
    return Fresher.query.count()


def get_all():
    return Fresher.query.order_by(Fresher.created_at.desc()).all()

