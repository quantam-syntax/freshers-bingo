from flask import Blueprint, jsonify
from app.auth.decorators import admin_required
from app.repositories import fresher_repo, challenge_repo, bingo_repo, winner_repo

stats_bp = Blueprint("stats", __name__, url_prefix="/api/stats")


@stats_bp.route("", methods=["GET"])
@admin_required
def get_stats():
    return jsonify({
        "freshers_registered": fresher_repo.count_all(),
        "challenges_total": challenge_repo.count_all(),
        "challenges_used": challenge_repo.get_used_count(),
        "bingo_completions": bingo_repo.count_completed(),
        "winners_count": winner_repo.count(),
    }), 200


@stats_bp.route("/freshers", methods=["GET"])
@admin_required
def get_freshers():
    freshers = fresher_repo.get_all()
    return jsonify([f.to_dict() for f in freshers]), 200

