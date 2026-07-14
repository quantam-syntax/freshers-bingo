from app.models.admin import Admin


def find_by_username(username):
    return Admin.query.filter_by(username=username).first()


def find_by_id(admin_id):
    return Admin.query.get(admin_id)
