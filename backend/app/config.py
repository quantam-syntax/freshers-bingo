import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
    }
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
    CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
