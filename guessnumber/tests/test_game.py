import random

import pytest

from guessnumber.game import (
    HIGHEST,
    LOWEST,
    check_guess,
    draw_secret,
    parse_guess,
    play,
)


@pytest.mark.parametrize(
    ("guess", "expected"),
    [(50, "correct"), (51, "too high"), (49, "too low")],
)
def test_check_guess(guess, expected):
    assert check_guess(guess, secret=50) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("42", 42),
        ("  7 \n", 7),
        (str(LOWEST), LOWEST),
        (str(HIGHEST), HIGHEST),
        ("0", None),
        ("1001", None),
        ("abc", None),
        ("", None),
        ("3.5", None),
    ],
)
def test_parse_guess(text, expected):
    assert parse_guess(text) == expected


def test_draw_secret_is_in_range_and_repeatable_with_seed():
    first = draw_secret(random.Random(123))
    second = draw_secret(random.Random(123))
    assert first == second
    assert LOWEST <= first <= HIGHEST


def run_game(secret, answers, max_tries=3):
    """Play a game with prepared answers instead of a keyboard."""
    inputs = iter(answers)
    output = []
    won = play(secret, max_tries, read=lambda _: next(inputs), write=output.append)
    return won, output


def test_player_wins():
    won, output = run_game(secret=500, answers=["250", "500"])
    assert won is True
    assert output[-1] == "Correct, you win! Tries used: 2."


def test_player_loses_after_all_tries():
    won, output = run_game(secret=500, answers=["1", "2", "3"])
    assert won is False
    assert output[-1] == "Game over! The number was 500."


def test_invalid_input_does_not_cost_a_try():
    won, output = run_game(secret=10, answers=["hello", "9", "11", "10"])
    assert won is True
    assert output[0].startswith("Please type a whole number")
    assert output[-1] == "Correct, you win! Tries used: 3."
