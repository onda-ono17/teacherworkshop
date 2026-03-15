import pytest
from httpx import ASGITransport, AsyncClient

from test_api import app


@pytest.mark.anyio
async def test_get_users_returns_seeded_users():
    transport = ASGITransport(app=app, lifespan="on")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/users")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 3
    assert body[0]["username"] == "alice"


@pytest.mark.anyio
async def test_get_user_by_id_success():
    transport = ASGITransport(app=app, lifespan="on")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/users/2")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 2
    assert body["username"] == "bob"
    assert body["email"] == "bob@example.com"
    assert "created_at" in body


@pytest.mark.anyio
async def test_get_user_by_id_not_found():
    transport = ASGITransport(app=app, lifespan="on")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.anyio
async def test_create_user_success():
    transport = ASGITransport(app=app, lifespan="on")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/users",
            json={"email": "dave@example.com", "username": "dave_01"},
        )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "dave@example.com"
    assert body["username"] == "dave_01"
    assert "id" in body
    assert "created_at" in body


@pytest.mark.anyio
async def test_create_user_duplicate_email_conflict():
    transport = ASGITransport(app=app, lifespan="on")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/users",
            json={"email": "alice@example.com", "username": "alice_dup"},
        )

    assert response.status_code == 409


@pytest.mark.anyio
async def test_patch_user_success():
    transport = ASGITransport(app=app, lifespan="on")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.patch("/users/3", json={"username": "charlie_new"})

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 3
    assert body["username"] == "charlie_new"


@pytest.mark.anyio
async def test_patch_user_not_found():
    transport = ASGITransport(app=app, lifespan="on")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.patch("/users/999", json={"username": "ghost_user"})

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.anyio
async def test_patch_user_duplicate_username_conflict():
    transport = ASGITransport(app=app, lifespan="on")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.patch("/users/3", json={"username": "alice"})

    assert response.status_code == 409


@pytest.mark.anyio
async def test_delete_user_success_then_not_found():
    transport = ASGITransport(app=app, lifespan="on")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        delete_response = await client.delete("/users/2")
        get_response = await client.get("/users/2")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


@pytest.mark.anyio
async def test_delete_user_not_found():
    transport = ASGITransport(app=app, lifespan="on")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
