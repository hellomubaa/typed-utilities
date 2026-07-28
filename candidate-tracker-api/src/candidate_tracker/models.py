"""Pydantic request/response models for the Candidate Tracker API."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator

# E.164-ish phone format: optional leading '+', then 7-15 digits.
# Separators (spaces, dashes, parentheses, dots) are stripped before matching.
_PHONE_RE = re.compile(r"^\+?\d{7,15}$")
_PHONE_STRIP_RE = re.compile(r"[\s\-().]")


def _normalize_phone(value: str) -> str:
    """Strip common separators and validate a phone number.

    Raises:
        ValueError: If the value is not a valid phone number.
    """
    stripped = _PHONE_STRIP_RE.sub("", value)
    if not _PHONE_RE.match(stripped):
        raise ValueError(
            "phone must be 7-15 digits, optionally prefixed with '+' "
            "(separators like spaces, dashes and parentheses are allowed)."
        )
    return stripped


class CandidateStatus(str, Enum):
    """Lifecycle stage of a candidate in the hiring pipeline."""

    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    HIRED = "hired"
    REJECTED = "rejected"


class CandidateBase(BaseModel):
    """Shared candidate fields used for create and update payloads."""

    name: str = Field(..., min_length=1, max_length=100, examples=["Ada Lovelace"])
    email: EmailStr = Field(..., examples=["ada@example.com"])
    phone: str = Field(..., examples=["+1 (555) 123-4567"])
    position: str = Field(
        ..., min_length=1, max_length=100, examples=["Backend Engineer"]
    )
    status: CandidateStatus = Field(default=CandidateStatus.APPLIED)

    @field_validator("name", "position")
    @classmethod
    def _strip_and_require_non_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank.")
        return cleaned

    @field_validator("phone")
    @classmethod
    def _validate_phone(cls, value: str) -> str:
        return _normalize_phone(value)


class CandidateCreate(CandidateBase):
    """Request body for creating a candidate."""


class CandidateUpdate(BaseModel):
    """Request body for partially updating a candidate (all fields optional)."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = None
    position: str | None = Field(default=None, min_length=1, max_length=100)
    status: CandidateStatus | None = None

    @field_validator("name", "position")
    @classmethod
    def _strip_and_require_non_empty(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank.")
        return cleaned

    @field_validator("phone")
    @classmethod
    def _validate_phone(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _normalize_phone(value)


class Candidate(CandidateBase):
    """Full candidate resource returned by the API."""

    id: int = Field(..., examples=[1])
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
