from flask import Blueprint, request, jsonify, g
from app.auth.decorators import fresher_required
from app.services import bingo_service
from app.extensions import socketio

bingo_bp = Blueprint("bingo", __name__, url_prefix="/api/bingo")


@bingo_bp.route("/me", methods=["GET"])
@fresher_required
def get_my_card():
    card = bingo_service.get_card(g.current_fresher.id)
    if not card:
        return jsonify({"error": "No bingo card found"}), 404
    return jsonify(card), 200


@bingo_bp.route("/cells/<int:cell_id>/upload", methods=["POST"])
@fresher_required
def upload_cell_photo(cell_id):
    if "photo" not in request.files:
        return jsonify({"error": "No photo file provided"}), 400

    photo = request.files["photo"]
    if photo.filename == "":
        return jsonify({"error": "No file selected"}), 400

    file_data = photo.read()
    content_type = photo.content_type or "image/jpeg"

    try:
        from app.storage.cloudinary_storage import upload_file
        photo_url = upload_file(file_data, content_type)
    except Exception:
        from app.storage.cloudinary_storage import upload_file_fallback
        photo_url = upload_file_fallback(file_data, content_type)

    card_data, winner_data = bingo_service.upload_cell_photo(cell_id, photo_url, g.current_fresher.id)
    if card_data is None:
        return jsonify({"error": winner_data}), 400

    if winner_data:
        socketio.emit("winners:update", winner_data)

    return jsonify({"card": card_data, "winner": winner_data}), 200
