"""In-memory storage backend for candidates.

This is intentionally simple (a dict keyed by id) so the API has no external
dependencies. Data is lost when the process restarts.
"""

from __future__ import annotations

from datetime import datetime, timezone

from .models import Candidate, CandidateCreate, CandidateUpdate


class CandidateStore:
    """A thread-unsafe, in-memory candidate store with auto-incrementing ids."""

    def __init__(self) -> None:
        self._items: dict[int, Candidate] = {}
        self._next_id: int = 1

    def list(self) -> list[Candidate]:
        """Return all candidates ordered by id."""
        return [self._items[key] for key in sorted(self._items)]

    def get(self, candidate_id: int) -> Candidate | None:
        """Return a candidate by id, or None if it does not exist."""
        return self._items.get(candidate_id)

    def email_exists(self, email: str, exclude_id: int | None = None) -> bool:
        """Return True if another candidate already uses this email."""
        target = email.lower()
        for candidate in self._items.values():
            if candidate.id == exclude_id:
                continue
            if str(candidate.email).lower() == target:
                return True
        return False

    def create(self, data: CandidateCreate) -> Candidate:
        """Create and store a new candidate."""
        candidate = Candidate(
            id=self._next_id,
            created_at=datetime.now(timezone.utc),
            **data.model_dump(),
        )
        self._items[candidate.id] = candidate
        self._next_id += 1
        return candidate

    def update(self, candidate_id: int, data: CandidateUpdate) -> Candidate | None:
        """Apply a partial update and return the candidate, or None if missing."""
        existing = self._items.get(candidate_id)
        if existing is None:
            return None
        changes = data.model_dump(exclude_unset=True)
        updated = existing.model_copy(update=changes)
        self._items[candidate_id] = updated
        return updated

    def delete(self, candidate_id: int) -> bool:
        """Delete a candidate. Return True if it existed, False otherwise."""
        return self._items.pop(candidate_id, None) is not None

    def clear(self) -> None:
        """Remove all candidates and reset the id counter (used in tests)."""
        self._items.clear()
        self._next_id = 1


# Module-level singleton used by the application.
store = CandidateStore()
