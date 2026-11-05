import uuid

from fastapi import status
from fastapi.testclient import TestClient

from utils.config import Configuration


def get_random_login() -> str:
    return f"user_{uuid.uuid4().hex[:8]}"


def test_registration_success(client: TestClient) -> None:
    login = get_random_login()
    response = client.post(
        "/api/register",
        json={"login": login, "password": "StrongPassword123!"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "message" in data
    assert "access_token" in data
    assert data["roles"] == ["user"]


def test_registration_duplicate_login(client: TestClient) -> None:
    login = get_random_login()
    client.post(
        "/api/register",
        json={"login": login, "password": "StrongPassword123!"},
    )

    response = client.post(
        "/api/register",
        json={"login": login, "password": "StrongPassword123!"},
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_registration_weak_password(client: TestClient) -> None:
    login = get_random_login()
    response = client.post(
        "/api/register",
        json={"login": login, "password": "123"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_forbidden_delete_for_regular_user(client: TestClient) -> None:
    login = get_random_login()
    reg_resp = client.post(
        "/api/register",
        json={"login": login, "password": "StrongPassword123!"},
    )
    user_token = reg_resp.json()["access_token"]

    msg_resp = client.post(
        "/api/messages",
        headers={"token": user_token},
        json={"text": "Hello world!"},
    )
    message_id = msg_resp.json()["message"]["id_"]

    del_resp = client.delete(
        f"/api/messages/{message_id}",
        headers={"token": user_token},
    )
    assert del_resp.status_code == status.HTTP_403_FORBIDDEN


def test_allowed_delete_for_moderator(client: TestClient) -> None:
    config = Configuration.from_env()
    admin_login_resp = client.post(
        "/api/login",
        json={"login": config.admin.login, "password": config.admin.password},
    )
    admin_token = admin_login_resp.json()["access_token"]
    alfredo_login = get_random_login()
    alfredo_resp = client.post(
        "/api/register",
        json={"login": alfredo_login, "password": "StrongPassword123!"},
    )
    alfredo_token = alfredo_resp.json()["access_token"]
    msg_resp = client.post(
        "/api/messages",
        headers={"token": alfredo_token},
        json={"text": "Hello World!"},
    )
    message_id = msg_resp.json()["message"]["id_"]
    role_resp = client.post(
        "/api/roles",
        headers={"token": admin_token},
        json={"target_login": alfredo_login, "roles": ["user", "moderator"]},
    )
    assert role_resp.status_code == status.HTTP_200_OK
    del_resp = client.delete(
        f"/api/messages/{message_id}",
        headers={"token": alfredo_token},
    )
    assert del_resp.status_code == status.HTTP_200_OK
