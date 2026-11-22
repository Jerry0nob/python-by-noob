# guessnumber

A small command-line game: guess a number from 1 to 1000 in 10 tries.

```bash
cd guessnumber
python -m guessnumber
```

```
I'm thinking of a number from 1 to 1000.
You have 10 tries.
Guess (1-1000): 500
You guessed too high! Tries left: 9.
Guess (1-1000): 250
You guessed too low! Tries left: 8.
...
```

## Why 10 tries?

If you always guess the middle of the remaining range (binary search), every
guess cuts the range in half. 2^10 = 1024, so 10 tries are always enough for
1000 numbers if you play smart.

## How it is built

- `game.py` keeps the logic in small functions (`parse_guess`, `check_guess`)
  that are easy to test.
- `play()` gets `read` and `write` functions as parameters. In the terminal they
  are `input()` and `print()`, in tests they are replaced with prepared answers.
- Invalid input (letters, numbers out of range) shows a message and does not
  cost a try.

## Tests

```bash
cd guessnumber
pytest
```

The tests run automatically on GitHub Actions on every push
(`.github/workflows/guessnumber.yml`).
