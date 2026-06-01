from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.deps import get_session
from models.consulta_model import ConsultaModel
from schemas.consulta_schema import ConsultaSchema

router = APIRouter()


@router.get(
    '/',
    response_model=List[ConsultaSchema],
    summary="Listar consultas",
    dependencies=[]
)
async def listar_consultas(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ConsultaModel)
        result = await session.execute(query)
        return result.scalars().all()


@router.get(
    '/{id_consulta}',
    response_model=ConsultaSchema,
    summary="Buscar consulta por ID",
    dependencies=[]
)
async def buscar_consulta(id_consulta: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ConsultaModel).filter(ConsultaModel.idConsulta == id_consulta)
        result = await session.execute(query)
        consulta = result.scalar_one_or_none()
        if not consulta:
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
        return consulta

