import uuid
import os
import cloudinary
import cloudinary.uploader
from app.config import Config

_initialized = False


def _init_cloudinary():
    global _initialized
    if _initialized:
        return
    cloudinary_url = Config.CLOUDINARY_URL
    if cloudinary_url:
        cloudinary.config(cloudinary_url=cloudinary_url)
        _initialized = True


def upload_file(file_data, content_type, folder="bingo-photos"):
    _init_cloudinary()
    file_ext = content_type.split("/")[-1] if "/" in content_type else "jpg"
    public_id = f"{folder}/{uuid.uuid4().hex}"

    result = cloudinary.uploader.upload(
        file_data,
        public_id=public_id,
        resource_type="image",
        format=file_ext,
        transformation=[
            {"width": 800, "height": 800, "crop": "limit", "quality": "auto"}
        ],
    )
    return result["secure_url"]


def upload_file_fallback(file_data, content_type, folder="bingo-photos"):
    file_ext = content_type.split("/")[-1] if "/" in content_type else "jpg"
    filename = f"{uuid.uuid4().hex}.{file_ext}"
    upload_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads", folder
    )
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    with open(filepath, "wb") as f:
        f.write(file_data)
    return f"/uploads/{folder}/{filename}"
