# typed-utils

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
git clone https://github.com/YOUR_USERNAME/typed-utils.git
cd typed-utils
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

Expected output:

```
32 passed
```

## Example usage

```python
from typed_utils.math_utils import divide
from typed_utils.string_utils import to_snake_case
from typed_utils.list_utils import chunk

divide(10, 2)                # 5.0
to_snake_case("Hello World")  # "hello_world"
chunk([1, 2, 3, 4, 5], 2)     # [[1, 2], [3, 4], [5]]
```

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

```bash
git checkout -b feature/typed-utils
git add .
git commit -m "Add typed utility package and pytest suite"
git push origin feature/typed-utils
```

Then open a pull request from `feature/typed-utils` into `main` for review
before merging.
