from app.extensions import db
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))


class Challenge(db.Model):
    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    is_used = db.Column(db.Boolean, default=False, index=True)
    used_at = db.Column(db.DateTime, nullable=True)
    created_by_admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))

    picks = db.relationship("ChallengePick", backref="challenge", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "is_used": self.is_used,
            "used_at": self.used_at.isoformat() if self.used_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class ChallengePick(db.Model):
    __tablename__ = "challenge_picks"

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    picked_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))
