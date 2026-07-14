import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from app.config import Config
from app.extensions import db
from app.repositories import fresher_repo, admin_repo
from app.services.bingo_service import generate_card_for_fresher

IST = timezone(timedelta(hours=5, minutes=30))


def create_fresher_token(fresher):
    payload = {
        "sub": str(fresher.id),
        "role": "fresher",
        "roll_no": fresher.roll_no,
        "exp": datetime.now(IST) + timedelta(days=30),
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")


def create_admin_token(admin):
    payload = {
        "sub": str(admin.id),
        "role": "admin",
        "username": admin.username,
        "exp": datetime.now(IST) + timedelta(days=7),
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")


def signup_fresher(roll_no, name, socials=None):
    existing = fresher_repo.find_by_roll_no(roll_no)
    if existing:
        token = create_fresher_token(existing)
        return {"fresher": existing.to_dict(), "token": token, "existing": True}

    fresher = fresher_repo.create(roll_no, name, socials)
    generate_card_for_fresher(fresher.id)
    db.session.commit()

    token = create_fresher_token(fresher)
    return {"fresher": fresher.to_dict(), "token": token, "existing": False}


def login_admin(username, password):
    admin = admin_repo.find_by_username(username)
    if not admin:
        return None

    if not bcrypt.checkpw(password.encode("utf-8"), admin.password_hash.encode("utf-8")):
        return None

    token = create_admin_token(admin)
    return {"admin": admin.to_dict(), "token": token}
