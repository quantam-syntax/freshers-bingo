import eventlet
eventlet.monkey_patch()

import bcrypt
from app import create_app
from app.extensions import db
from app.models.admin import Admin
from app.models.challenge import Challenge

SAMPLE_CHALLENGES = [
    "Do 10 jumping jacks right now.",
    "Find someone wearing the same color shirt as you and take a selfie.",
    "Sing the chorus of your favorite song out loud.",
    "Do your best impression of a celebrity.",
    "Find someone born in the same month as you.",
    "Do a 30-second plank.",
    "Tell a joke to a group and make them laugh.",
    "Find someone from a different state than you.",
    "Do the moonwalk across the room.",
    "Find someone who has the same favorite movie as you.",
    "Find someone wearing glasses and compliment them.",
    "Share your best life advice in 10 seconds.",
    "Do your best animal impression.",
    "Take a selfie making the funniest face you can.",
    "Do a victory dance right where you are.",
    "Tell someone near you a genuine compliment.",
    "Tell the group your hidden talent.",
    "Find someone from your department and take a selfie.",
    "Sing \"Happy Birthday\" to a random person.",
    "Do your best Bollywood dance move.",
    "Take a selfie with someone you just met.",
    "Do 10 squats while counting loudly.",
    "Share your favorite childhood memory.",
    "Do a tongue twister three times fast.",
    "Take a group selfie with at least 5 people.",
    "Do the floss dance for 15 seconds.",
    "Do a robot dance for 10 seconds.",
    "Tell a two-sentence horror story.",
    "Do a penguin walk across the room.",
    "Do a freeze dance , dance for 10 seconds, then freeze instantly when the host says \"STOP!\""
]


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        existing_admin = Admin.query.filter_by(username="admin").first()
        if not existing_admin:
            password_hash = bcrypt.hashpw("freshers2026".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            admin = Admin(username="admin", password_hash=password_hash)
            db.session.add(admin)
            db.session.commit()
            admin_id = admin.id
            print("Admin created: admin / freshers2026")
        else:
            admin_id = existing_admin.id
            print("Admin already exists")

        # Delete all existing challenges to replace them with the new list
        Challenge.query.delete()
        db.session.commit()
        print("Deleted existing challenges")

        for text in SAMPLE_CHALLENGES:
            challenge = Challenge(text=text, created_by_admin_id=admin_id)
            db.session.add(challenge)
        db.session.commit()
        print(f"Seeded {len(SAMPLE_CHALLENGES)} new challenges")


if __name__ == "__main__":
    seed()
