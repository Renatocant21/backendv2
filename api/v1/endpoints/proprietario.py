from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.deps import get_session, get_usuario_atual, exigir_admin
from models.proprietario_model import ProprietarioModel
from schemas.proprietario_schema import ProprietarioSchema

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ProprietarioSchema,
    summary="Cadastrar proprietário",
    dependencies=[Depends(exigir_admin)]
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
    dependencies=[Depends(get_usuario_atual)]
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
    dependencies=[Depends(get_usuario_atual)]
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
    dependencies=[Depends(exigir_admin)]
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
    dependencies=[Depends(exigir_admin)]
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
