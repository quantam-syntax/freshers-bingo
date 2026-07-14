import eventlet
eventlet.monkey_patch()

import bcrypt
from app import create_app
from app.extensions import db
from app.models.admin import Admin
from app.models.challenge import Challenge

SAMPLE_CHALLENGES = [
    "Do 10 jumping jacks right now",
    "Find someone wearing the same color shirt as you and take a selfie",
    "Sing the chorus of your favorite song out loud",
    "Do your best impression of a celebrity",
    "Show the last photo in your camera roll to a stranger",
    "Find someone born in the same month as you",
    "Do a 30-second plank",
    "Tell a joke to a group of strangers and make them laugh",
    "Find someone from a different state than you",
    "Do the moonwalk across the room",
    "Take a selfie with the nearest plant",
    "Find someone who has the same favorite movie as you",
    "Do 5 push-ups in front of everyone",
    "Share your most embarrassing childhood story",
    "Find someone wearing glasses and compliment them",
    "Do a dramatic reading of the last text you sent",
    "Find someone taller than you and stand back-to-back",
    "Share your best life advice in 10 seconds",
    "Find someone who plays the same sport as you",
    "Do your best animal impression",
    "Take a selfie making the funniest face you can",
    "Find someone who has visited the same country as you",
    "Recite the alphabet backwards as fast as you can",
    "Find someone who shares your taste in music",
    "Do a victory dance right where you are",
    "Tell someone near you a genuine compliment",
    "Find someone who has the same number of siblings as you",
    "Take a selfie doing a yoga pose",
    "Share your favorite food and why you love it",
    "Find someone who uses the same phone brand as you",
    "Do a cartwheel or attempt one",
    "Tell the group your hidden talent",
    "Find someone who watches the same TV show as you",
    "Do 20 high knees in place",
    "Share the meaning behind your name",
    "Find someone from your department and take a selfie",
    "Sing Happy Birthday to a random person",
    "Find someone who has a pet and share pet stories",
    "Do a dramatic entrance into a room",
    "Share your biggest dream with a stranger",
    "Find someone left-handed",
    "Do your best Bollywood dance move",
    "Take a selfie with someone you just met",
    "Find someone who knows the same programming language",
    "Do 10 squats while counting loudly",
    "Share your favorite childhood memory",
    "Find someone who wakes up before 6 AM",
    "Do a tongue twister three times fast",
    "Take a group selfie with at least 5 people",
    "Find someone who can solve a Rubiks cube",
    "Do an impression of your favorite teacher",
    "Share the last song you listened to",
    "Find someone wearing sneakers and race them",
    "Do a freeze dance — dance then freeze on command",
    "Tell a stranger your most unpopular opinion",
    "Find someone who reads books regularly",
    "Do the floss dance for 15 seconds",
    "Share what you would do with a million dollars",
    "Find someone born in a different country",
    "Do air guitar to an imaginary song",
    "Tell the group your favorite meme",
    "Find someone who is a morning person",
    "Do a trust fall with a new friend",
    "Share your go-to karaoke song",
    "Find someone who loves cooking and share recipes",
    "Do 5 star jumps",
    "Tell everyone your most used emoji",
    "Find someone who binge-watches shows",
    "Do a slow-motion replay of catching a ball",
    "Share your bucket list item number one",
    "Find someone who speaks more than 2 languages",
    "Do a robot dance for 10 seconds",
    "Tell a two-sentence horror story",
    "Find someone who loves coffee and debate tea vs coffee",
    "Do a wall sit for 20 seconds",
    "Share the funniest thing that happened to you this week",
    "Find someone wearing earrings",
    "Do an accent challenge — speak in a British accent for 30 seconds",
    "Tell the group your comfort movie",
    "Find someone who is a night owl",
    "Do a penguin walk across the room",
    "Share your favorite quote",
    "Find someone who journals regularly",
    "Do a handshake with 5 different people",
    "Tell everyone your dream travel destination",
    "Find someone who plays a musical instrument",
    "Do a photobomb in someone elses selfie",
    "Share what superpower you would want",
    "Find someone who likes the same ice cream flavor",
    "Do a crab walk for 5 meters",
    "Tell a dad joke to a group",
    "Find someone who has attended a concert",
    "Do a dramatic movie scene reenactment",
    "Share your favorite childhood cartoon",
    "Find someone wearing a watch",
    "Do a balancing act — stand on one foot for 15 seconds",
    "Tell the group about a skill you want to learn",
    "Find someone who volunteers or does community service",
    "Do an imaginary cooking show for 20 seconds",
    "Share your most-played song on Spotify",
    "Find someone who is an only child",
    "Do a fashion runway walk",
    "Tell everyone your favorite school subject",
    "Find someone who can whistle a tune",
    "Do a pretend news anchor reading",
    "Share your comfort food",
    "Find someone who likes hiking or trekking",
    "Do a limbo under an imaginary bar",
    "Tell the group your unpopular food opinion",
    "Find someone who collects something",
    "Do your best superhero pose",
    "Share what you were doing exactly 24 hours ago",
    "Find someone who has a birthday this month",
    "Do a speed round — name 10 fruits in 10 seconds",
    "Tell everyone a fun fact about yourself",
    "Find someone from the same city as you",
    "Do a mirroring game with a partner for 30 seconds",
    "Share your most-used app besides social media",
    "Find someone who has dyed their hair",
    "Do an invisible jump rope for 15 seconds",
    "Tell the group the last movie you cried watching",
    "Find someone who does yoga or meditation",
    "Do a silly walk from one end of the room to the other",
    "Share your earliest memory",
    "Find someone who has gone skydiving or bungee jumping",
    "Do a mime act — pretend to be stuck in a box",
    "Tell everyone your go-to comfort show",
    "Find someone who likes board games",
    "Do a dramatic gasp and point at nothing",
    "Share the weirdest food combination you enjoy",
    "Find someone who has the same zodiac sign",
    "Do a beatbox attempt for 10 seconds",
    "Tell the group your dream job as a kid vs now",
    "Find someone who can do a magic trick",
    "Do a finger gun battle with someone",
    "Share your most replayed YouTube video",
    "Find someone who has pulled an all-nighter this week",
    "Do a headstand or attempt one against a wall",
    "Tell everyone what you would name your autobiography",
    "Find someone who is ambidextrous",
    "Do a charades round — act out a movie title",
    "Share the best advice you ever received",
    "Find someone who has been on a road trip",
    "Do a speed walk race with someone nearby",
    "Tell the group your spirit animal and why",
    "Find someone who has tried a new cuisine recently",
    "Do a dramatic slow clap that builds up",
    "Share your favorite holiday tradition",
    "Find someone who likes the same season as you",
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

        existing_count = Challenge.query.count()
        if existing_count == 0:
            for text in SAMPLE_CHALLENGES:
                challenge = Challenge(text=text, created_by_admin_id=admin_id)
                db.session.add(challenge)
            db.session.commit()
            print(f"Seeded {len(SAMPLE_CHALLENGES)} challenges")
        else:
            print(f"Challenges already exist ({existing_count})")


if __name__ == "__main__":
    seed()
