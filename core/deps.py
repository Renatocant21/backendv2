from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import Session
from core.security import decodificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()


async def get_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_session)
):
    from models.usuario_model import UsuarioModel

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decodificar_token(token)
    if payload is None:
        raise credentials_exception

    login: Optional[str] = payload.get("sub")
    if login is None:
        raise credentials_exception

    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.Login == login)
        result = await session.execute(query)
        usuario = result.scalar_one_or_none()

    if usuario is None:
        raise credentials_exception
    return usuario


def exigir_admin(usuario=Depends(get_usuario_atual)):
    if usuario.tipoUsuario != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return usuario
