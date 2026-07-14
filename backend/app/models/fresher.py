from app.extensions import db
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))


class Fresher(db.Model):
    __tablename__ = "freshers"

    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    socials = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))

    bingo_card = db.relationship("BingoCard", backref="fresher", uselist=False, lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "roll_no": self.roll_no,
            "name": self.name,
            "socials": self.socials,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
