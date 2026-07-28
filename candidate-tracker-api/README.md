# Candidate Tracker API

A small, tested **FastAPI** CRUD service for tracking job candidates through a
hiring pipeline. State is kept **in memory** (no database), so it is easy to run
locally and demonstrates REST principles, Pydantic validation, meaningful HTTP
status codes, and auto-generated OpenAPI/Swagger docs.

## What it does

Manage `Candidate` resources with full CRUD:

| Method   | Path                     | Purpose                       | Success | Errors        |
| -------- | ------------------------ | ----------------------------- | ------- | ------------- |
| `GET`    | `/candidates`            | List candidates (filterable)  | `200`   | —             |
| `GET`    | `/candidates/{id}`       | Get one candidate             | `200`   | `404`         |
| `POST`   | `/candidates`            | Create a candidate            | `201`   | `409`, `422`  |
| `PUT`    | `/candidates/{id}`       | Update (partial) a candidate  | `200`   | `404`, `409`, `422` |
| `DELETE` | `/candidates/{id}`       | Delete a candidate            | `204`   | `404`         |
| `GET`    | `/health`                | Liveness probe                | `200`   | —             |

`GET /candidates` accepts an optional `?status=` query parameter to filter by
pipeline stage.

### The `Candidate` resource

| Field        | Type     | Rules                                                        |
| ------------ | -------- | ----------------------------------------------------------- |
| `id`         | int      | Server-generated, read-only                                 |
| `name`       | string   | Required, 1–100 chars, trimmed, not blank                   |
| `email`      | string   | Required, must be a valid email, **unique** across records  |
| `phone`      | string   | Required, 7–15 digits, optional `+`; separators normalized  |
| `position`   | string   | Required, 1–100 chars, trimmed, not blank                   |
| `status`     | enum     | One of `applied`, `screening`, `interview`, `offer`, `hired`, `rejected` (default `applied`) |
| `created_at` | datetime | Server-generated, read-only                                 |

## REST & HTTP semantics used here

- **Methods are verbs:** `GET` reads, `POST` creates, `PUT` updates, `DELETE` removes.
- **Meaningful status codes:** `201 Created` on create, `204 No Content` on
  delete, `404 Not Found` for missing ids, `409 Conflict` for duplicate emails,
  and `422 Unprocessable Entity` (from Pydantic) for malformed input.
- **Validation:** malformed emails and phone numbers are rejected automatically
  with a `422` and a detailed error body.

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the server

```bash
uvicorn candidate_tracker.main:app --reload --app-dir src
```

Then open:

- Interactive Swagger docs: <http://127.0.0.1:8000/docs>
- ReDoc docs: <http://127.0.0.1:8000/redoc>
- OpenAPI schema: <http://127.0.0.1:8000/openapi.json>

### Try it with curl

```bash
# Create
curl -X POST http://127.0.0.1:8000/candidates \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada Lovelace","email":"ada@example.com","phone":"+1 (555) 123-4567","position":"Backend Engineer"}'

# List
curl http://127.0.0.1:8000/candidates

# Filter by status
curl "http://127.0.0.1:8000/candidates?status=applied"

# Get one
curl http://127.0.0.1:8000/candidates/1

# Update (partial)
curl -X PUT http://127.0.0.1:8000/candidates/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"interview"}'

# Delete
curl -X DELETE http://127.0.0.1:8000/candidates/1
```

## Running the tests

```bash
python -m pytest -v
```

Tests use `pytest` + FastAPI's `TestClient` (backed by `httpx`) and run with
coverage automatically (configured in `pyproject.toml`); the suite fails if
total coverage drops below 90%.

## Project structure

```
candidate-tracker-api/
├── src/candidate_tracker/
│   ├── __init__.py
│   ├── main.py        # FastAPI app + routes
│   ├── models.py      # Pydantic request/response models + validation
│   └── storage.py     # in-memory store
├── tests/
│   ├── conftest.py           # fixtures (TestClient, store reset)
│   ├── test_candidates.py    # CRUD behavior
│   └── test_validation.py    # email/phone/field validation
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Notes

- Storage is in memory, so all data is lost when the server restarts.
- Emails are treated as unique; creating or updating to a duplicate returns `409`.
