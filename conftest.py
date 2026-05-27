import allure
import json
import pytest
import os

import requests


def attach_json(name: str, payload: object) -> None:
    allure.attach(
        json.dumps(payload, ensure_ascii=False, indent=2),
        name=name,
        attachment_type=allure.attachment_type.JSON
    )

@pytest.fixture(scope='session')
def base_url() -> str:
    return os.getenv("TEST_API_BASE_URL", "").rstrip("/")

@pytest.fixture(scope='session')
def student_email() -> str:
    value = os.getenv("TEST_STUDENT_EMAIL", "").strip()
    if not value:
        pytest.fail("TEST_STUDENT_EMAIL is required")
    return value

@pytest.fixture(scope='session')
def student_password() -> str:
    value = os.getenv("TEST_STUDENT_PASSWORD", "").strip()
    if not value:
        pytest.fail("TEST_STUDENT_PASSWORD is required")
    return value

@pytest.fixture(scope='session')
def access_token(base_url, student_email, student_password):
    payload = {
        "email": student_email,
        "password": student_password
    }

    with allure.step("Get access token"):
        response = requests.post(
            f"{base_url}/auth/login",
            json=payload,
            timeout=10
        )
        attach_json("login-response", response.json())

    assert response.status_code == 200
    return response.json()['access_token']

@pytest.fixture()
def api_client(base_url, access_token):
    with requests.Session() as session:
        session.base_url = base_url
        session.headers.update(
            {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        yield session