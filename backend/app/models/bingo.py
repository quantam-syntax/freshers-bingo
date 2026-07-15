from app.extensions import db
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))


class BingoCard(db.Model):
    __tablename__ = "bingo_cards"

    id = db.Column(db.Integer, primary_key=True)
    fresher_id = db.Column(db.Integer, db.ForeignKey("freshers.id"), unique=True, nullable=False)
    win_mode = db.Column(db.String(20), default="any_line")
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST))

    cells = db.relationship("BingoCell", backref="bingo_card", lazy="joined", order_by="BingoCell.position")

    def to_dict(self):
        return {
            "id": self.id,
            "fresher_id": self.fresher_id,
            "win_mode": self.win_mode,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "cells": [c.to_dict() for c in self.cells],
            "filled_count": sum(1 for c in self.cells if c.photo_url is not None),
            "total_count": len(self.cells),
        }


BINGO_TASKS = {
    "1": "Someone who knows more than 3 languages",
    "2": "Someone who can dance",
    "3": "Someone who can juggle",
    "4": "Someone who can drive",
    "5": "Someone who can cook a 3-course meal",
    "6": "Someone who has met a celebrity",
    "7": "Someone who has more than 1k followers on Instagram",
    "8": "Someone who has read more than 5 books last year",
    "9": "Can solve a Rubik's Cube",
    "10": "Can do a magic trick",
    "11": "Uses Linux",
    "12": "Has the same favorite movie as you",
    "13": "Can recite a poem from memory",
    "14": "Has built a game",
    "15": "Has written a program over 500 lines",
    "16": "Knows web dev",
    "17": "Knows a programming language other than Python",
    "18": "Someone who lived outside India",
    "19": "Someone who is left handed",
    "20": "Someone who knows sign language",
    "21": "Has the same birthday as you",
    "22": "Has broken a bone",
    "23": "Plays an instrument",
    "24": "Has a pet"
}


class BingoCell(db.Model):
    __tablename__ = "bingo_cells"

    id = db.Column(db.Integer, primary_key=True)
    bingo_card_id = db.Column(db.Integer, db.ForeignKey("bingo_cards.id"), nullable=False, index=True)
    position = db.Column(db.Integer, nullable=False)
    letter = db.Column(db.String(5), nullable=False)
    photo_url = db.Column(db.Text, nullable=True)
    filled_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        is_center = self.position == 12
        task_text = "Solo selfie!" if is_center else BINGO_TASKS.get(self.letter, "")
        return {
            "id": self.id,
            "position": self.position,
            "letter": self.letter,
            "task_text": task_text,
            "photo_url": self.photo_url,
            "filled_at": self.filled_at.isoformat() if self.filled_at else None,
            "is_center": is_center,
        }
