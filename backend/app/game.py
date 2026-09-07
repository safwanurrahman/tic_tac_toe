from typing import Literal


Player = Literal["red", "green"]
Board = list[Player | None]

WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def get_winner(board: Board) -> Player | None:
    for first, second, third in WINNING_LINES:
        player = board[first]

        if player is not None and player == board[second] == board[third]:
            return player

    return None


def is_draw(board: Board) -> bool:
    return get_winner(board) is None and None not in board