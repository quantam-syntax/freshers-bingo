#!/usr/bin/env python3
"""Cloudinary onboarding test — upload, inspect, and transform an image."""

import cloudinary
import cloudinary.uploader
import cloudinary.api

# ──────────────────────────────────────────────
# 1. Configure Cloudinary (inline credentials)
# ──────────────────────────────────────────────
cloudinary.config(
    cloud_name="bow93prb",
    api_key="744198743215262",
    api_secret="DikYteyZFCU4Rxz70L50z3hDHeg",
    secure=True,
)

print("✅ Cloudinary configured\n")

# ──────────────────────────────────────────────
# 2. Upload a sample image from Cloudinary's demo domain
# ──────────────────────────────────────────────
sample_url = "https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg"

print(f"⬆️  Uploading image from: {sample_url}")
upload_result = cloudinary.uploader.upload(
    sample_url,
    public_id="onboarding_test/shoes",
    overwrite=True,
    resource_type="image",
)

secure_url = upload_result["secure_url"]
public_id = upload_result["public_id"]

print(f"   Secure URL : {secure_url}")
print(f"   Public ID  : {public_id}\n")

# ──────────────────────────────────────────────
# 3. Get image details (metadata)
# ──────────────────────────────────────────────
print("🔍 Fetching image metadata...")
details = cloudinary.api.resource(public_id)

print(f"   Width      : {details['width']} px")
print(f"   Height     : {details['height']} px")
print(f"   Format     : {details['format']}")
print(f"   Size       : {details['bytes']} bytes\n")

# ──────────────────────────────────────────────
# 4. Transform the image
#    f_auto — automatically selects the best format
#             (e.g. WebP, AVIF) based on the browser
#    q_auto — automatically adjusts quality to reduce
#             file size while keeping visual fidelity
# ──────────────────────────────────────────────
transformed_url = cloudinary.utils.cloudinary_url(
    public_id,
    fetch_format="auto",   # f_auto
    quality="auto",        # q_auto
)[0]

print("🎉 Done! Click the link below to see the optimized version of the image.")
print("   Check the size and the format.\n")
print(f"   🔗 {transformed_url}")
