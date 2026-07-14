from flask import Blueprint, jsonify
from app.services import winner_service

winners_bp = Blueprint("winners", __name__, url_prefix="/api/winners")


@winners_bp.route("", methods=["GET"])
def get_winners():
    winners = winner_service.get_winners()
    return jsonify(winners), 200
