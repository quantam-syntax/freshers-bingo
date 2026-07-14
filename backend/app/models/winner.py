from app.extensions import db
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))


class Winner(db.Model):
    __tablename__ = "winners"

    id = db.Column(db.Integer, primary_key=True)
    fresher_id = db.Column(db.Integer, db.ForeignKey("freshers.id"), nullable=False)
    bingo_card_id = db.Column(db.Integer, db.ForeignKey("bingo_cards.id"), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))

    fresher = db.relationship("Fresher", backref="winner_entry", uselist=False)
    bingo_card = db.relationship("BingoCard", backref="winner_entry", uselist=False)

    def to_dict(self):
        center_cell = None
        if self.bingo_card and self.bingo_card.cells:
            for cell in self.bingo_card.cells:
                if cell.position == 12:
                    center_cell = cell.photo_url
                    break
        return {
            "id": self.id,
            "rank": self.rank,
            "fresher_name": self.fresher.name if self.fresher else None,
            "fresher_roll_no": self.fresher.roll_no if self.fresher else None,
            "solo_selfie_url": center_cell,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
