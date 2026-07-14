import jwt
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))
secret = "dev-secret-key-change-in-production"

payload = {
    "sub": 1,
    "role": "fresher",
    "roll_no": "123",
    "exp": datetime.now(IST) + timedelta(days=30),
}
print("Original payload:", payload)
token = jwt.encode(payload, secret, algorithm="HS256")
print("Token:", token)

try:
    decoded = jwt.decode(token, secret, algorithms=["HS256"])
    print("Decoded:", decoded)
except Exception as e:
    print("Error:", type(e), e)
