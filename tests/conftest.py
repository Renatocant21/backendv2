import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app
from core.configs import DBBaseModel
from core.deps import get_session

TEST_DB_URL = "sqlite+aiosqlite:///./test.db"

engine_test = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)


async def override_get_session():
    session = TestSession()
    try:
        yield session
    finally:
        await session.close()


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture(scope="session", autouse=True)
async def criar_tabelas():
    async with engine_test.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def token_admin(client: AsyncClient):
    await client.post("/api/v1/usuarios/", json={
        "Nome": "Admin Teste",
        "Login": "admin",
        "Senha": "admin123",
        "email": "admin@teste.com",
        "tipoUsuario": "admin"
    })
    resp = await client.post("/api/v1/auth/login", data={"username": "admin", "password": "admin123"})
    return resp.json()["access_token"]


@pytest_asyncio.fixture
async def token_usuario(client: AsyncClient):
    await client.post("/api/v1/usuarios/", json={
        "Nome": "Usuário Comum",
        "Login": "comum",
        "Senha": "comum123",
        "email": "comum@teste.com",
        "tipoUsuario": "operador"
    })
    resp = await client.post("/api/v1/auth/login", data={"username": "comum", "password": "comum123"})
    return resp.json()["access_token"]
