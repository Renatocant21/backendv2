from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.deps import get_session, get_usuario_atual, exigir_admin
from core.security import hash_senha
from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchema, UsuarioCriarSchema

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=UsuarioSchema,
    summary="Criar usuário",
    description="Cria novo usuário. Senha é armazenada com hash bcrypt."
)
async def criar_usuario(usuario: UsuarioCriarSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.Login == usuario.Login)
        result = await session.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Login já cadastrado")

        novo_usuario = UsuarioModel(
            Nome=usuario.Nome,
            Login=usuario.Login,
            Senha=hash_senha(usuario.Senha),
            email=usuario.email,
            tipoUsuario=usuario.tipoUsuario
        )
        session.add(novo_usuario)
        await session.commit()
        await session.refresh(novo_usuario)
        return novo_usuario


@router.get(
    '/',
    response_model=List[UsuarioSchema],
    summary="Listar usuários",
    dependencies=[]
)
async def listar_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        return result.scalars().all()


@router.get(
    '/me',
    response_model=UsuarioSchema,
    summary="Meu perfil"
)
async def meu_perfil(usuario_atual=Depends(get_usuario_atual)):
    return usuario_atual


@router.get(
    '/{id_usuario}',
    response_model=UsuarioSchema,
    summary="Buscar usuário por ID",
    dependencies=[]
)
async def buscar_usuario(id_usuario: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.idUsuario == id_usuario)
        result = await session.execute(query)
        usuario = result.scalar_one_or_none()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return usuario


@router.put(
    '/{id_usuario}',
    response_model=UsuarioSchema,
    summary="Atualizar usuário",
    dependencies=[]
)
async def atualizar_usuario(
    id_usuario: int,
    usuario: UsuarioCriarSchema,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.idUsuario == id_usuario)
        result = await session.execute(query)
        usuario_up = result.scalar_one_or_none()
        if not usuario_up:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        usuario_up.Nome = usuario.Nome
        usuario_up.Login = usuario.Login
        usuario_up.Senha = hash_senha(usuario.Senha)
        usuario_up.email = usuario.email
        usuario_up.tipoUsuario = usuario.tipoUsuario
        await session.commit()
        await session.refresh(usuario_up)
        return usuario_up


@router.delete(
    '/{id_usuario}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar usuário",
    dependencies=[]
)
async def deletar_usuario(id_usuario: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.idUsuario == id_usuario)
        result = await session.execute(query)
        usuario = result.scalar_one_or_none()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        await session.delete(usuario)
        await session.commit()

