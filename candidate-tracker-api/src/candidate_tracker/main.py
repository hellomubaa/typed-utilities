"""FastAPI application exposing CRUD endpoints for candidates."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query, Response, status

from .models import Candidate, CandidateCreate, CandidateStatus, CandidateUpdate
from .storage import CandidateStore, store

app = FastAPI(
    title="Candidate Tracker API",
    version="0.1.0",
    description=(
        "A small, in-memory REST API for tracking job candidates through a "
        "hiring pipeline. Demonstrates FastAPI routing, Pydantic validation, "
        "meaningful HTTP status codes, and OpenAPI/Swagger docs at /docs."
    ),
)


def get_store() -> CandidateStore:
    """Return the active candidate store (indirection kept for testability)."""
    return store


@app.get("/health", tags=["meta"], summary="Liveness probe")
def health() -> dict[str, str]:
    """Return a simple status payload to confirm the service is running."""
    return {"status": "ok"}


@app.get(
    "/candidates",
    response_model=list[Candidate],
    tags=["candidates"],
    summary="List candidates",
)
def list_candidates(
    status_filter: CandidateStatus | None = Query(
        default=None,
        alias="status",
        description="Filter candidates by pipeline status.",
    ),
) -> list[Candidate]:
    """Return all candidates, optionally filtered by status."""
    candidates = get_store().list()
    if status_filter is not None:
        candidates = [c for c in candidates if c.status == status_filter]
    return candidates


@app.get(
    "/candidates/{candidate_id}",
    response_model=Candidate,
    tags=["candidates"],
    summary="Get a candidate by id",
    responses={404: {"description": "Candidate not found"}},
)
def get_candidate(candidate_id: int) -> Candidate:
    """Return a single candidate by id, or 404 if it does not exist."""
    candidate = get_store().get(candidate_id)
    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate {candidate_id} not found.",
        )
    return candidate


@app.post(
    "/candidates",
    response_model=Candidate,
    status_code=status.HTTP_201_CREATED,
    tags=["candidates"],
    summary="Create a candidate",
    responses={409: {"description": "Email already in use"}},
)
def create_candidate(payload: CandidateCreate) -> Candidate:
    """Create a new candidate and return it with a generated id."""
    active = get_store()
    if active.email_exists(str(payload.email)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A candidate with email '{payload.email}' already exists.",
        )
    return active.create(payload)


@app.put(
    "/candidates/{candidate_id}",
    response_model=Candidate,
    tags=["candidates"],
    summary="Update a candidate",
    responses={
        404: {"description": "Candidate not found"},
        409: {"description": "Email already in use"},
    },
)
def update_candidate(candidate_id: int, payload: CandidateUpdate) -> Candidate:
    """Partially update a candidate. Only provided fields are changed."""
    active = get_store()
    if active.get(candidate_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate {candidate_id} not found.",
        )
    if payload.email is not None and active.email_exists(
        str(payload.email), exclude_id=candidate_id
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A candidate with email '{payload.email}' already exists.",
        )
    updated = active.update(candidate_id, payload)
    assert updated is not None  # existence checked above
    return updated


@app.delete(
    "/candidates/{candidate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["candidates"],
    summary="Delete a candidate",
    responses={404: {"description": "Candidate not found"}},
)
def delete_candidate(candidate_id: int) -> Response:
    """Delete a candidate by id. Returns 204 on success, 404 if not found."""
    if not get_store().delete(candidate_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate {candidate_id} not found.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
