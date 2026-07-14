from functools import wraps
from flask import request, jsonify, g
import jwt
from app.config import Config
from app.models.fresher import Fresher
from app.models.admin import Admin


def fresher_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        if not token:
            return jsonify({"error": "Token required"}), 401
        try:
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            if payload.get("role") != "fresher":
                return jsonify({"error": "Fresher access required"}), 403
            fresher = Fresher.query.get(payload["sub"])
            if not fresher:
                return jsonify({"error": "Fresher not found"}), 404
            g.current_fresher = fresher
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        if not token:
            return jsonify({"error": "Token required"}), 401
        try:
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            if payload.get("role") != "admin":
                return jsonify({"error": "Admin access required"}), 403
            admin = Admin.query.get(payload["sub"])
            if not admin:
                return jsonify({"error": "Admin not found"}), 404
            g.current_admin = admin
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated
