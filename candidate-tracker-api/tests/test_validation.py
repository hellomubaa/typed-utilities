"""Input validation tests: malformed emails, phones, and missing fields."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "bad_email",
    ["not-an-email", "missing@domain", "@no-local.com", "spaces in@email.com"],
)
def test_rejects_malformed_email(
    client: TestClient, sample_payload: dict[str, str], bad_email: str
) -> None:
    response = client.post(
        "/candidates", json={**sample_payload, "email": bad_email}
    )
    assert response.status_code == 422


@pytest.mark.parametrize(
    "bad_phone",
    ["123", "phone-number", "+", "12345678901234567890", "555-CALL-NOW"],
)
def test_rejects_malformed_phone(
    client: TestClient, sample_payload: dict[str, str], bad_phone: str
) -> None:
    response = client.post(
        "/candidates", json={**sample_payload, "phone": bad_phone}
    )
    assert response.status_code == 422


@pytest.mark.parametrize("field", ["name", "email", "phone", "position"])
def test_rejects_missing_required_field(
    client: TestClient, sample_payload: dict[str, str], field: str
) -> None:
    payload = {k: v for k, v in sample_payload.items() if k != field}
    response = client.post("/candidates", json=payload)
    assert response.status_code == 422


def test_rejects_blank_name(
    client: TestClient, sample_payload: dict[str, str]
) -> None:
    response = client.post(
        "/candidates", json={**sample_payload, "name": "   "}
    )
    assert response.status_code == 422


def test_rejects_invalid_status(
    client: TestClient, sample_payload: dict[str, str]
) -> None:
    response = client.post(
        "/candidates", json={**sample_payload, "status": "ghosted"}
    )
    assert response.status_code == 422


def test_validation_error_has_detail(
    client: TestClient, sample_payload: dict[str, str]
) -> None:
    response = client.post(
        "/candidates", json={**sample_payload, "email": "bad"}
    )
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert isinstance(body["detail"], list)


def test_accepts_valid_international_phone(
    client: TestClient, sample_payload: dict[str, str]
) -> None:
    response = client.post(
        "/candidates", json={**sample_payload, "phone": "+44 20 7946 0958"}
    )
    assert response.status_code == 201
    assert response.json()["phone"] == "+442079460958"
