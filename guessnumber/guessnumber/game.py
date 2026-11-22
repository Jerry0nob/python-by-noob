"""Number guessing game: the player has a limited number of tries."""

import random
from collections.abc import Callable
from typing import Literal

LOWEST = 1
HIGHEST = 1000
MAX_TRIES = 10  # enough for binary search: 2**10 = 1024 >= 1000 numbers

Hint = Literal["correct", "too high", "too low"]


def draw_secret(rng: random.Random | None = None) -> int:
    """Return a random secret number between LOWEST and HIGHEST."""
    rng = rng or random.Random()
    return rng.randint(LOWEST, HIGHEST)


def parse_guess(text: str) -> int | None:
    """Turn user input into a number in range, or None if it is not valid."""
    try:
        number = int(text.strip())
    except ValueError:
        return None
    if not LOWEST <= number <= HIGHEST:
        return None
    return number


def check_guess(guess: int, secret: int) -> Hint:
    """Compare the guess with the secret number."""
    if guess == secret:
        return "correct"
    if guess > secret:
        return "too high"
    return "too low"


def play(
    secret: int,
    max_tries: int = MAX_TRIES,
    read: Callable[[str], str] = input,
    write: Callable[[str], None] = print,
) -> bool:
    """Run one game. Return True if the player guessed the number.

    `read` and `write` default to input() and print(), but tests can pass
    their own functions, so the game can be tested without a keyboard.
    """
    tries_left = max_tries
    while tries_left > 0:
        guess = parse_guess(read(f"Guess ({LOWEST}-{HIGHEST}): "))
        if guess is None:
            write(f"Please type a whole number from {LOWEST} to {HIGHEST}.")
            continue  # an invalid input does not cost a try

        tries_left -= 1
        hint = check_guess(guess, secret)
        if hint == "correct":
            write(f"Correct, you win! Tries used: {max_tries - tries_left}.")
            return True
        write(f"You guessed {hint}! Tries left: {tries_left}.")

    write(f"Game over! The number was {secret}.")
    return False
