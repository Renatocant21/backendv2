from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session
from models.relatorio_model import RelatorioModel
from schemas.relatorio_schema import RelatorioCriarSchema, RelatorioSchema

router = APIRouter()


@router.get(
    "/",
    response_model=List[RelatorioSchema],
    summary="Listar todos os relatórios",
    description="Retorna todos os relatórios. Requer autenticação."
)
async def listar_relatorios(
    db: AsyncSession = Depends(get_session),
    usuario_atual=Depends(get_usuario_atual)
):
    async with db as session:
        result = await session.execute(select(RelatorioModel))
        return result.scalars().all()


@router.get(
    "/{idRelatorio}",
    response_model=RelatorioSchema,
    summary="Buscar relatório por ID"
)
async def buscar_relatorio(
    idRelatorio: int,
    db: AsyncSession = Depends(get_session),
    usuario_atual=Depends(get_usuario_atual)
):
    async with db as session:
        result = await session.execute(
            select(RelatorioModel).filter(RelatorioModel.idRelatorio == idRelatorio)
        )
        relatorio = result.scalar_one_or_none()
    if not relatorio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relatório não encontrado")
    return relatorio


@router.post(
    "/",
    response_model=RelatorioSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Criar relatório"
)
async def criar_relatorio(
    dados: RelatorioCriarSchema,
    db: AsyncSession = Depends(get_session),
    usuario_atual=Depends(get_usuario_atual)
):
    novo = RelatorioModel(**dados.model_dump())
    async with db as session:
        session.add(novo)
        await session.commit()
        await session.refresh(novo)
    return novo


@router.delete(
    "/{idRelatorio}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir relatório"
)
async def excluir_relatorio(
    idRelatorio: int,
    db: AsyncSession = Depends(get_session),
    usuario_atual=Depends(get_usuario_atual)
):
    async with db as session:
        result = await session.execute(
            select(RelatorioModel).filter(RelatorioModel.idRelatorio == idRelatorio)
        )
        relatorio = result.scalar_one_or_none()
        if not relatorio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relatório não encontrado")
        await session.delete(relatorio)
        await session.commit()

