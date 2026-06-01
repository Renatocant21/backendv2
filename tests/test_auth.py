import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_criar_usuario(client: AsyncClient):
    resp = await client.post("/api/v1/usuarios/", json={
        "Nome": "Teste Silva",
        "Login": "testemarcador",
        "Senha": "senha123",
        "email": "teste@marca.com",
        "tipoUsuario": "operador"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["Login"] == "testemarcador"
    assert "Senha" not in data  # senha nunca deve aparecer na resposta


@pytest.mark.asyncio
async def test_login_sucesso(client: AsyncClient):
    await client.post("/api/v1/usuarios/", json={
        "Nome": "Login User",
        "Login": "loginuser",
        "Senha": "pass1234",
        "email": "login@user.com",
        "tipoUsuario": "operador"
    })
    resp = await client.post("/api/v1/auth/login", data={"username": "loginuser", "password": "pass1234"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_senha_errada(client: AsyncClient):
    resp = await client.post("/api/v1/auth/login", data={"username": "loginuser", "password": "errada"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_endpoint_protegido_sem_token(client: AsyncClient):
    resp = await client.get("/api/v1/veiculos/")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_meu_perfil(client: AsyncClient, token_usuario: str):
    resp = await client.get("/api/v1/usuarios/me", headers={"Authorization": f"Bearer {token_usuario}"})
    assert resp.status_code == 200
    assert resp.json()["Login"] == "comum"


@pytest.mark.asyncio
async def test_listar_usuarios_sem_admin(client: AsyncClient, token_usuario: str):
    resp = await client.get("/api/v1/usuarios/", headers={"Authorization": f"Bearer {token_usuario}"})
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_listar_usuarios_admin(client: AsyncClient, token_admin: str):
    resp = await client.get("/api/v1/usuarios/", headers={"Authorization": f"Bearer {token_admin}"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
