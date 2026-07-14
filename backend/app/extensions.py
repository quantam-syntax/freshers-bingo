import os
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS

_origins = os.environ.get("ALLOWED_ORIGINS", "*")
allowed_origins = _origins if _origins == "*" else [o.strip() for o in _origins.split(",")]

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins=allowed_origins, async_mode="eventlet")
cors = CORS()

