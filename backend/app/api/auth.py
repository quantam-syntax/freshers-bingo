from flask import Blueprint, request, jsonify
from app.schemas.auth_schema import SignupSchema, AdminLoginSchema
from app.services import auth_service

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

@auth_bp.route("/debug/jwt", methods=["GET"])
def debug_jwt():
    import jwt
    from app.config import Config
    test_secret = Config.JWT_SECRET
    token = jwt.encode({"test": "data"}, test_secret, algorithm="HS256")
    try:
        decoded = jwt.decode(token, test_secret, algorithms=["HS256"])
        success = True
        err = None
    except Exception as e:
        success = False
        err = str(e)
    return jsonify({
        "secret_length": len(test_secret) if test_secret else 0,
        "secret_starts_with": test_secret[:3] if test_secret else None,
        "token": token,
        "success": success,
        "error": err
    })


signup_schema = SignupSchema()
admin_login_schema = AdminLoginSchema()


@auth_bp.route("/auth/signup", methods=["POST"])
def signup():
    data = request.get_json()
    errors = signup_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    result = auth_service.signup_fresher(
        roll_no=data["roll_no"],
        name=data["name"],
    )
    status = 200 if result["existing"] else 201
    return jsonify(result), status


@auth_bp.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    errors = admin_login_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    result = auth_service.login_admin(data["username"], data["password"])
    if not result:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify(result), 200
