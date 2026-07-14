from flask import Blueprint, request, jsonify, g
from app.auth.decorators import admin_required
from app.schemas.challenge_schema import ChallengeSchema
from app.services import challenge_service
from app.extensions import socketio

challenges_bp = Blueprint("challenges", __name__, url_prefix="/api/challenges")

challenge_schema = ChallengeSchema()


@challenges_bp.route("", methods=["GET"])
@admin_required
def list_challenges():
    challenges = challenge_service.get_all_challenges()
    return jsonify(challenges), 200


@challenges_bp.route("", methods=["POST"])
@admin_required
def add_challenge():
    data = request.get_json()
    errors = challenge_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    challenge = challenge_service.add_challenge(data["text"], g.current_admin.id)
    return jsonify(challenge), 201


@challenges_bp.route("/<int:challenge_id>", methods=["PUT"])
@admin_required
def update_challenge(challenge_id):
    data = request.get_json()
    errors = challenge_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    challenge = challenge_service.update_challenge(challenge_id, data["text"])
    if not challenge:
        return jsonify({"error": "Challenge not found"}), 404
    return jsonify(challenge), 200


@challenges_bp.route("/<int:challenge_id>", methods=["DELETE"])
@admin_required
def delete_challenge(challenge_id):
    success = challenge_service.delete_challenge(challenge_id)
    if not success:
        return jsonify({"error": "Challenge not found"}), 404
    return jsonify({"message": "Deleted"}), 200


@challenges_bp.route("/pick", methods=["POST"])
@admin_required
def pick_challenge():
    challenge, reel_payload = challenge_service.pick_random_challenge()
    if not challenge:
        return jsonify({"error": "No unused challenges remaining"}), 400

    socketio.emit("challenge:picking", reel_payload)
    socketio.emit("challenge:picked", challenge)

    return jsonify({"challenge": challenge, "reel": reel_payload}), 200


@challenges_bp.route("/<int:challenge_id>/undo", methods=["POST"])
@admin_required
def undo_challenge(challenge_id):
    challenge = challenge_service.undo_challenge(challenge_id)
    if not challenge:
        return jsonify({"error": "Challenge not found"}), 404
    return jsonify(challenge), 200
