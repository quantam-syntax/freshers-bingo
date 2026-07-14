import random
from app.repositories import challenge_repo


REEL_SIZE = 18


def get_all_challenges():
    return [c.to_dict() for c in challenge_repo.get_all()]


def add_challenge(text, admin_id):
    challenge = challenge_repo.create(text, admin_id)
    return challenge.to_dict()


def update_challenge(challenge_id, text):
    challenge = challenge_repo.find_by_id(challenge_id)
    if not challenge:
        return None
    challenge = challenge_repo.update(challenge, text)
    return challenge.to_dict()


def delete_challenge(challenge_id):
    challenge = challenge_repo.find_by_id(challenge_id)
    if not challenge:
        return False
    challenge_repo.delete(challenge)
    return True


def pick_random_challenge():
    unused = challenge_repo.get_unused()
    if not unused:
        return None, None

    chosen = random.choice(unused)

    reel_pool = [c.text for c in unused if c.id != chosen.id]
    if len(reel_pool) < REEL_SIZE - 1:
        reel_pool = reel_pool * ((REEL_SIZE // max(len(reel_pool), 1)) + 1)

    reel = random.sample(reel_pool, min(REEL_SIZE - 1, len(reel_pool)))
    final_index = len(reel)
    reel.append(chosen.text)

    challenge_repo.mark_used(chosen)

    reel_payload = {
        "reel": reel,
        "final_index": final_index,
        "challenge": chosen.to_dict(),
    }
    return chosen.to_dict(), reel_payload


def undo_challenge(challenge_id):
    challenge = challenge_repo.find_by_id(challenge_id)
    if not challenge:
        return None
    challenge = challenge_repo.mark_unused(challenge)
    return challenge.to_dict()
