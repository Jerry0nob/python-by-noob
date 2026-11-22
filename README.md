# python-by-noob

My Python learning repository. Each folder is a small, separate project with
its own tests and its own GitHub Actions pipeline.

| Project | What it is | CI |
|---|---|---|
| [guessnumber](guessnumber/) | Command-line number guessing game | ![guessnumber CI](https://github.com/Jerry0nob/python-by-noob/actions/workflows/guessnumber.yml/badge.svg) |
| [matplotlib_basics](matplotlib_basics/) | First charts with matplotlib and numpy | ![matplotlib_basics CI](https://github.com/Jerry0nob/python-by-noob/actions/workflows/matplotlib_basics.yml/badge.svg) |
| [portscan](portscan/) | TCP connect port scanner (work in progress) | - |

## How the pipelines work

Every project has a workflow in `.github/workflows/`. It runs only when files of
that project change, and on Python 3.11-3.14 it checks:

1. `ruff check` - linting (errors, unused imports, import order),
2. `ruff format --check` - code formatting,
3. `pytest` - tests.
