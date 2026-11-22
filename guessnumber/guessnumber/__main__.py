"""Entry point: python -m guessnumber"""

from guessnumber.game import HIGHEST, LOWEST, MAX_TRIES, draw_secret, play


def main() -> None:
    print(f"I'm thinking of a number from {LOWEST} to {HIGHEST}.")
    print(f"You have {MAX_TRIES} tries.")
    play(draw_secret())


if __name__ == "__main__":
    main()
