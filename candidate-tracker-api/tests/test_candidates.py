"""CRUD behavior tests for the Candidate Tracker API."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _create(client: TestClient, payload: dict[str, str]) -> dict[str, object]:
    response = client.post("/candidates", json=payload)
    assert response.status_code == 201
    return response.json()


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_candidate_returns_201_and_id(
    client: TestClient, sample_payload: dict[str, str]
) -> None:
    body = _create(client, sample_payload)
    assert body["id"] == 1
    assert body["name"] == "Ada Lovelace"
    assert body["email"] == "ada@example.com"
    # Phone separators are normalized away.
    assert body["phone"] == "+15551234567"
    assert "created_at" in body


def test_create_normalizes_and_trims(client: TestClient) -> None:
    body = _create(
        client,
        {
            "name": "  Grace Hopper  ",
            "email": "grace@example.com",
            "phone": "555-987-6543",
            "position": "  Compiler Engineer  ",
        },
    )
    assert body["name"] == "Grace Hopper"
    assert body["position"] == "Compiler Engineer"
    assert body["phone"] == "5559876543"
    # Status defaults to "applied" when omitted.
    assert body["status"] == "applied"


def test_list_candidates_empty(client: TestClient) -> None:
    response = client.get("/candidates")
    assert response.status_code == 200
    assert response.json() == []


def test_list_candidates_returns_all(
    client: TestClient, sample_payload: dict[str, str]
) -> None:
    _create(client, sample_payload)
    _create(client, {**sample_payload, "email": "second@example.com"})
    response = client.get("/candidates")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_candidates_filter_by_status(
    client: TestClient, sample_payload: dict[str, str]
) -> None:
    _create(client, sample_payload)
    _create(
        client,
        {**sample_payload, "email": "hired@example.com", "status": "hired"},
    )
    response = client.get("/candidates", params={"status": "hired"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "hired"


def test_get_candidate_found(
    client: TestClient, sample_payload: dict[str, str]
) -> None:
    created = _create(client, sample_payload)
    response = client.get(f"/candidates/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_candidate_not_found(client: TestClient) -> None:
    response = client.get("/candidates/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_candidate_partial(
    client: TestClient, sample_payload: dict[str, str]
) -> None:
    created = _create(client, sample_payload)
    response = client.put(
        f"/candidates/{created['id']}", json={"status": "interview"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "interview"
    # Untouched fields remain unchanged.
    assert body["name"] == "Ada Lovelace"


def test_update_candidate_not_found(client: TestClient) -> None:
    response = client.put("/candidates/999", json={"status": "offer"})
    assert response.status_code == 404


def test_delete_candidate(
    client: TestClient, sample_payload: dict[str, str]
) -> None:
    created = _create(client, sample_payload)
    response = client.delete(f"/candidates/{created['id']}")
    assert response.status_code == 204
    # It is gone now.
    assert client.get(f"/candidates/{created['id']}").status_code == 404


def test_delete_candidate_not_found(client: TestClient) -> None:
    response = client.delete("/candidates/999")
    assert response.status_code == 404


def test_duplicate_email_returns_409(
    client: TestClient, sample_payload: dict[str, str]
) -> None:
    _create(client, sample_payload)
    response = client.post("/candidates", json=sample_payload)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


def test_update_to_existing_email_returns_409(
    client: TestClient, sample_payload: dict[str, str]
) -> None:
    _create(client, sample_payload)
    second = _create(
        client, {**sample_payload, "email": "second@example.com"}
    )
    response = client.put(
        f"/candidates/{second['id']}", json={"email": "ada@example.com"}
    )
    assert response.status_code == 409
