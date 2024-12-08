from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def get_token(
    username: str,
    password: str,
    token_endpoint: str = 'api/auth'
):
    return client.post(
        url=token_endpoint,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={'username': username, 'password': password}
    )

