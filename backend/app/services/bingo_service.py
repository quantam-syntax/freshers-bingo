import random
from app.repositories import bingo_repo, winner_repo

WEIGHTED_LETTERS = list("AAABBBCCCDDDEEEFFFGGGHHHIIIJJJKKKLLLMMMNNNOOOPPPRRRSSSTTTUUUVVVWWYYY")

BINGO_LINES = [
    [0, 1, 2, 3, 4],
    [5, 6, 7, 8, 9],
    [10, 11, 12, 13, 14],
    [15, 16, 17, 18, 19],
    [20, 21, 22, 23, 24],
    [0, 5, 10, 15, 20],
    [1, 6, 11, 16, 21],
    [2, 7, 12, 17, 22],
    [3, 8, 13, 18, 23],
    [4, 9, 14, 19, 24],
    [0, 6, 12, 18, 24],
    [4, 8, 12, 16, 20],
]


def generate_card_for_fresher(fresher_id):
    letters = []
    for i in range(25):
        if i == 12:
            letters.append("★")
        else:
            letters.append(random.choice(WEIGHTED_LETTERS))
    return bingo_repo.create_card(fresher_id, letters)


def get_card(fresher_id):
    card = bingo_repo.find_by_fresher_id(fresher_id)
    if not card:
        return None
    return card.to_dict()


def upload_cell_photo(cell_id, photo_url, fresher_id):
    cell = bingo_repo.find_cell_by_id(cell_id)
    if not cell:
        return None, "Cell not found"

    card = cell.bingo_card
    if card.fresher_id != fresher_id:
        return None, "Not your card"

    bingo_repo.update_cell_photo(cell, photo_url)

    completed = check_completion(card)
    winner_data = None
    if completed and not card.completed_at:
        bingo_repo.mark_card_completed(card)
        winner = winner_repo.add_winner(fresher_id, card.id)
        if winner:
            winner_data = winner.to_dict()

    return card.to_dict(), winner_data


def check_completion(card):
    filled_positions = set()
    for cell in card.cells:
        if cell.photo_url is not None:
            filled_positions.add(cell.position)

    if card.win_mode == "any_line":
        for line in BINGO_LINES:
            if all(pos in filled_positions for pos in line):
                return True
        return False

    return len(filled_positions) == 25
