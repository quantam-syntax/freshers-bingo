import os
from flask import Flask, send_from_directory
from app.config import Config
from app.extensions import db, socketio, cors, allowed_origins


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    socketio.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": allowed_origins}})

    from app.api.auth import auth_bp
    from app.api.challenges import challenges_bp
    from app.api.bingo import bingo_bp
    from app.api.winners import winners_bp
    from app.api.stats import stats_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(challenges_bp)
    app.register_blueprint(bingo_bp)
    app.register_blueprint(winners_bp)
    app.register_blueprint(stats_bp)

    from app.sockets import register_socket_handlers
    register_socket_handlers(socketio)

    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    @app.route("/uploads/<path:filename>")
    def serve_upload(filename):
        return send_from_directory(upload_dir, filename)

    with app.app_context():
        from app.models import fresher, admin, challenge, bingo, winner
        db.create_all()

    return app
