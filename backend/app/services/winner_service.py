from app.repositories import winner_repo


def get_winners():
    winners = winner_repo.get_all()
    return [w.to_dict() for w in winners]


def winner_count():
    return winner_repo.count()
