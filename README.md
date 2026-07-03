# typed-utils

[![Python Tests](https://github.com/hellomubaa/typed-utilities/actions/workflows/python-tests.yml/badge.svg)](https://github.com/hellomubaa/typed-utilities/actions/workflows/python-tests.yml)

A small, typed Python utility package with math, string, and list helper
functions — built to demonstrate type hints, clean project structure,
virtual environments, and pytest testing.

## Package contents

- `typed_utils.math_utils` — add, subtract, multiply, divide, average, clamp
- `typed_utils.string_utils` — reverse, is_palindrome, word_count, truncate, to_snake_case
- `typed_utils.list_utils` — flatten, unique, chunk, find_first

All functions use type hints and raise `ValueError` on invalid input
(e.g. dividing by zero, averaging an empty list).

## Setup

Clone the repository:

```bash
git clone https://github.com/hellomubaa/typed-utilities.git
cd typed-utilities
```

Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the tests

```bash
python -m pytest -v
```

Tests run with coverage automatically (configured in `pyproject.toml`) and the
suite fails if total coverage drops below 80%. Current coverage is ~99%.
Expected output:

```
33 passed
Required test coverage of 80% reached. Total coverage: 99.08%
```

## Type checking

The package is fully type-hinted. Run static type checking in strict mode with
`mypy`:

```bash
# strict type check of the package
python -m mypy --strict src

# run tests
python -m pytest -v
```

Both commands should pass with no errors. `mypy` configuration lives in
`pyproject.toml` under `[tool.mypy]` (strict mode enabled).

## Linting and formatting

Code style is enforced with [`ruff`](https://docs.astral.sh/ruff/) (linter and
formatter) and [`black`](https://black.readthedocs.io/) (formatter). Both use a
line length of 88 and produce the same style, so either can format the code.

```bash
# lint
python -m ruff check src tests

# check formatting (use the same commands without --check to auto-format)
python -m ruff format --check src tests
python -m black --check src tests
```

Style configuration lives in `pyproject.toml` under `[tool.ruff]` and
`[tool.black]`.

## How to run quality gates locally

These are the same gates enforced in CI. After activating your virtual
environment and installing dependencies (`pip install -r requirements.txt`),
run all four gates with one command:

```bash
python -m ruff check src tests && python -m ruff format --check src tests && python -m black --check src tests && python -m mypy --strict src && python -m pytest --cov
```

Or run them individually:

```bash
python -m ruff check src tests        # lint
python -m ruff format --check src tests  # formatting (ruff)
python -m black --check src tests     # formatting (black)
python -m mypy --strict src           # strict type checking
python -m pytest --cov                # tests + coverage (fails under 80%)
```

All five commands must pass before pushing. Configuration for each tool lives
in `pyproject.toml`.

## Example usage

```python
from typed_utils.math_utils import divide
from typed_utils.string_utils import to_snake_case
from typed_utils.list_utils import chunk

divide(10, 2)                # 5.0
to_snake_case("Hello World")  # "hello_world"
chunk([1, 2, 3, 4, 5], 2)     # [[1, 2], [3, 4], [5]]
```

## Edge-case behavior

The helpers have well-defined behavior for boundary and invalid inputs:

- **`truncate(text, max_length, suffix="...")`** — returns `text` unchanged when
  it already fits within `max_length`. When it must cut and `max_length` is
  less than or equal to the suffix length, only the (clipped) suffix is
  returned, e.g. `truncate("hello world", 2) == ".."`. A negative `max_length`
  raises `ValueError`.
- **`chunk(items, size)`** — splits into consecutive chunks of at most `size`;
  the final chunk may be shorter. An empty list returns `[]`. A `size` that is
  zero or negative raises `ValueError`.
- **`unique(items)`** — removes duplicates while preserving first-seen order
  (not sorted). Items must be hashable.
- **`to_snake_case(text)`** — lowercases, converts camelCase boundaries and
  whitespace to single underscores, collapses repeated underscores, and strips
  leading/trailing underscores, e.g. `to_snake_case("  Hello World ") ==
  "hello_world"`. An empty string returns `""`.

## Project structure

```
typed-utils/
├── src/typed_utils/
│   ├── __init__.py
│   ├── math_utils.py
│   ├── string_utils.py
│   └── list_utils.py
├── tests/
│   ├── test_math_utils.py
│   ├── test_string_utils.py
│   └── test_list_utils.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Git workflow used for this project

The project follows a feature-branch + pull-request workflow:

```bash
git checkout -b feature/typed-utils
git add .
git commit -m "Add typed utility package and pytest suite"
git push origin feature/typed-utils
```

Changes are opened as a pull request, reviewed, and merged into the default
branch. Continuous integration (GitHub Actions: **Python Tests**) runs `ruff`,
`mypy`, and `pytest` on every push and pull request — the current status is
shown by the badge at the top of this README.

### Pull request evidence

A representative merged pull request with its passing CI run:

- Merged PR: https://github.com/hellomubaa/typed-utilities/pull/2
- Passing CI run for that PR: https://github.com/hellomubaa/typed-utilities/actions/runs/28684145219

For the complete trail:

- All pull requests: https://github.com/hellomubaa/typed-utilities/pulls?q=is%3Apr
- All CI runs: https://github.com/hellomubaa/typed-utilities/actions

Each pull request is merged only after the **Python Tests** workflow
(`ruff` + `black` + `mypy --strict` + `pytest` with coverage) passes.
