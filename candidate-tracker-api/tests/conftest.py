"""Shared pytest fixtures for the Candidate Tracker API tests."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from candidate_tracker.main import app
from candidate_tracker.storage import store


@pytest.fixture(autouse=True)
def _reset_store() -> Iterator[None]:
    """Ensure every test starts with an empty in-memory store."""
    store.clear()
    yield
    store.clear()


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Return a FastAPI TestClient bound to the application."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_payload() -> dict[str, str]:
    """Return a valid candidate creation payload."""
    return {
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "phone": "+1 (555) 123-4567",
        "position": "Backend Engineer",
        "status": "applied",
    }
