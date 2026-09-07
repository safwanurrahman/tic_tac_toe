from app.game import get_winner, is_draw


def test_red_wins_with_top_row():
    board = [
        "red", "red", "red",
        None, "green", None,
        "green", None, None,
    ]

    assert get_winner(board) == "red"


def test_green_wins_diagonally():
    board = [
        "green", "red", None,
        "red", "green", None,
        None, None, "green",
    ]

    assert get_winner(board) == "green"


def test_game_has_no_winner():
    board = [
        "red", None, None,
        None, "green", None,
        None, None, None,
    ]

    assert get_winner(board) is None


def test_full_board_is_draw():
    board = [
        "red", "green", "red",
        "red", "green", "green",
        "green", "red", "red",
    ]

    assert is_draw(board) is True


def test_incomplete_board_is_not_draw():
    board = [
        "red", "green", None,
        None, None, None,
        None, None, None,
    ]

    assert is_draw(board) is False