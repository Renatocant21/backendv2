from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.deps import get_session
from models.operacao_model import OperacaoModel
from schemas.operacao_schema import OperacaoSchema

router = APIRouter()


@router.get(
    '/',
    response_model=List[OperacaoSchema],
    summary="Listar operações",
    dependencies=[]
)
async def listar_operacoes(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(OperacaoModel).order_by(OperacaoModel.dataHora.desc())
        result = await session.execute(query)
        return result.scalars().all()


@router.get(
    '/usuario/{id_usuario}',
    response_model=List[OperacaoSchema],
    summary="Operações por usuário",
    dependencies=[]
)
async def buscar_operacoes_por_usuario(id_usuario: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(OperacaoModel).filter(
            OperacaoModel.idUsuario == id_usuario
        ).order_by(OperacaoModel.dataHora.desc())
        result = await session.execute(query)
        return result.scalars().all()

