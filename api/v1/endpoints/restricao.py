from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.deps import get_session
from models.restricao_model import RestricaoModel
from models.veiculo_model import VeiculoModel
from schemas.restricao_schema import RestricaoSchema

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=RestricaoSchema,
    summary="Registrar restrição",
    dependencies=[]
)
async def criar_restricao(restricao: RestricaoSchema, db: AsyncSession = Depends(get_session)):
    nova_restricao = RestricaoModel(Placa=restricao.Placa, tipoRestricao=restricao.tipoRestricao)
    db.add(nova_restricao)
    query = select(VeiculoModel).filter(VeiculoModel.Placa == restricao.Placa)
    result = await db.execute(query)
    veiculo = result.scalar_one_or_none()
    if veiculo:
        veiculo.Situacao = restricao.tipoRestricao
    await db.commit()
    return nova_restricao


@router.get(
    '/',
    response_model=List[RestricaoSchema],
    summary="Listar restrições",
    dependencies=[]
)
async def listar_restricoes(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RestricaoModel)
        result = await session.execute(query)
        return result.scalars().all()


@router.get(
    '/{placa}',
    response_model=RestricaoSchema,
    summary="Buscar restrição por placa",
    dependencies=[]
)
async def buscar_restricao(placa: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RestricaoModel).filter(RestricaoModel.Placa == placa)
        result = await session.execute(query)
        restricao = result.scalar_one_or_none()
        if not restricao:
            raise HTTPException(status_code=404, detail="Restrição não encontrada")
        return restricao


@router.delete(
    '/{placa}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover restrição",
    dependencies=[]
)
async def deletar_restricao(placa: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RestricaoModel).filter(RestricaoModel.Placa == placa)
        result = await session.execute(query)
        restricao = result.scalar_one_or_none()
        if not restricao:
            raise HTTPException(status_code=404, detail="Restrição não encontrada")
        await session.delete(restricao)
        query_veic = select(VeiculoModel).filter(VeiculoModel.Placa == placa)
        result_veic = await session.execute(query_veic)
        veiculo = result_veic.scalar_one_or_none()
        if veiculo:
            veiculo.Situacao = 'REGULAR'
        await session.commit()

