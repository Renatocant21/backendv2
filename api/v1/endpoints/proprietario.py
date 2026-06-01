from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.deps import get_session
from models.proprietario_model import ProprietarioModel
from schemas.proprietario_schema import ProprietarioSchema

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ProprietarioSchema,
    summary="Cadastrar proprietário",
    dependencies=[]
)
async def criar_proprietario(prop: ProprietarioSchema, db: AsyncSession = Depends(get_session)):
    novo_proprietario = ProprietarioModel(CPF=prop.CPF, Nome=prop.Nome)
    db.add(novo_proprietario)
    await db.commit()
    return novo_proprietario


@router.get(
    '/',
    response_model=List[ProprietarioSchema],
    summary="Listar proprietários",
    dependencies=[]
)
async def listar_proprietarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProprietarioModel)
        result = await session.execute(query)
        return result.scalars().all()


@router.get(
    '/{cpf}',
    response_model=ProprietarioSchema,
    summary="Buscar proprietário por CPF",
    dependencies=[]
)
async def buscar_proprietario(cpf: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProprietarioModel).filter(ProprietarioModel.CPF == cpf)
        result = await session.execute(query)
        proprietario = result.scalar_one_or_none()
        if not proprietario:
            raise HTTPException(status_code=404, detail="Proprietário não encontrado")
        return proprietario


@router.put(
    '/{cpf}',
    response_model=ProprietarioSchema,
    summary="Atualizar proprietário",
    dependencies=[]
)
async def atualizar_proprietario(cpf: str, prop: ProprietarioSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProprietarioModel).filter(ProprietarioModel.CPF == cpf)
        result = await session.execute(query)
        proprietario = result.scalar_one_or_none()
        if not proprietario:
            raise HTTPException(status_code=404, detail="Proprietário não encontrado")
        proprietario.Nome = prop.Nome
        await session.commit()
        return proprietario


@router.delete(
    '/{cpf}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar proprietário",
    dependencies=[]
)
async def deletar_proprietario(cpf: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProprietarioModel).filter(ProprietarioModel.CPF == cpf)
        result = await session.execute(query)
        proprietario = result.scalar_one_or_none()
        if not proprietario:
            raise HTTPException(status_code=404, detail="Proprietário não encontrado")
        await session.delete(proprietario)
        await session.commit()


