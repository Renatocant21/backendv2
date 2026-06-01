import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_criar_proprietario_e_veiculo(client: AsyncClient, token_admin: str):
    headers = {"Authorization": f"Bearer {token_admin}"}

    resp_prop = await client.post("/api/v1/proprietarios/", json={
        "CPF": "12345678901",
        "Nome": "João da Silva"
    }, headers=headers)
    assert resp_prop.status_code == 201

    resp_veic = await client.post("/api/v1/veiculos/", json={
        "Placa": "ABC1234",
        "Chassi": "9BWZZZ377VT004251",
        "Modelo": "Civic",
        "Marca": "Honda",
        "Cor": "Prata",
        "Situacao": "REGULAR",
        "CPFProprietario": "12345678901"
    }, headers=headers)
    assert resp_veic.status_code == 201
    assert resp_veic.json()["Placa"] == "ABC1234"


@pytest.mark.asyncio
async def test_listar_veiculos_autenticado(client: AsyncClient, token_usuario: str):
    resp = await client.get("/api/v1/veiculos/", headers={"Authorization": f"Bearer {token_usuario}"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_criar_veiculo_sem_permissao(client: AsyncClient, token_usuario: str):
    resp = await client.post("/api/v1/veiculos/", json={
        "Placa": "XYZ9999",
        "Chassi": "9BWZZZ377VT009999",
        "Modelo": "Gol",
        "Marca": "VW",
        "Cor": "Branco",
        "Situacao": "REGULAR",
        "CPFProprietario": "12345678901"
    }, headers={"Authorization": f"Bearer {token_usuario}"})
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_consultar_placa(client: AsyncClient, token_usuario: str):
    resp = await client.get(
        "/api/v1/veiculos/consultar/ABC1234",
        headers={"Authorization": f"Bearer {token_usuario}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["Placa"] == "ABC1234"
    assert "Situacao" in data
    assert "Mensagem" in data


@pytest.mark.asyncio
async def test_consultar_placa_inexistente(client: AsyncClient, token_usuario: str):
    resp = await client.get(
        "/api/v1/veiculos/consultar/ZZZ9999",
        headers={"Authorization": f"Bearer {token_usuario}"}
    )
    assert resp.status_code == 404
