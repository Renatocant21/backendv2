from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.deps import get_session, get_usuario_atual, exigir_admin
from models.veiculo_model import VeiculoModel
from models.proprietario_model import ProprietarioModel
from models.consulta_model import ConsultaModel
from schemas.veiculo_schema import VeiculoSchema, ConsultaPlacaResponse
from datetime import datetime

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=VeiculoSchema,
    summary="Cadastrar veículo",
    dependencies=[Depends(exigir_admin)]
)
async def criar_veiculo(veic: VeiculoSchema, db: AsyncSession = Depends(get_session)):
    novo_veiculo = VeiculoModel(
        Placa=veic.Placa, Chassi=veic.Chassi, Modelo=veic.Modelo,
        Marca=veic.Marca, Cor=veic.Cor, Situacao=veic.Situacao,
        CPFProprietario=veic.CPFProprietario
    )
    db.add(novo_veiculo)
    await db.commit()
    return novo_veiculo


@router.get(
    '/',
    response_model=List[VeiculoSchema],
    summary="Listar veículos",
    dependencies=[Depends(get_usuario_atual)]
)
async def listar_veiculos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VeiculoModel)
        result = await session.execute(query)
        return result.scalars().all()


@router.get(
    '/consultar/{placa}',
    response_model=ConsultaPlacaResponse,
    summary="Consultar placa",
    description="Retorna situação do veículo e registra a consulta no histórico."
)
async def consultar_placa(
    placa: str,
    db: AsyncSession = Depends(get_session),
    usuario_atual=Depends(get_usuario_atual)
):
    async with db as session:
        query = select(VeiculoModel, ProprietarioModel).join(
            ProprietarioModel, VeiculoModel.CPFProprietario == ProprietarioModel.CPF
        ).filter(VeiculoModel.Placa == placa)
        result = await session.execute(query)
        row = result.first()

        if not row:
            raise HTTPException(status_code=404, detail="Placa não encontrada")

        veiculo, proprietario = row
        mensagem = (
            "ALERTA: Veículo ROUBADO/FURTADO!"
            if veiculo.Situacao == "ROUBO/FURTO"
            else "Veículo REGULAR"
        )

        consulta = ConsultaModel(
            Placa=placa,
            idUsuario=usuario_atual.idUsuario,
            tipoConsulta='automatica',
            dataHora=datetime.now(),
            Resultado=veiculo.Situacao
        )
        session.add(consulta)
        await session.commit()

        return ConsultaPlacaResponse(
            Placa=veiculo.Placa, Situacao=veiculo.Situacao, Mensagem=mensagem,
            Proprietario=proprietario.Nome, Modelo=veiculo.Modelo or '',
            Marca=veiculo.Marca or '', Cor=veiculo.Cor or ''
        )


@router.get(
    '/{placa}',
    response_model=VeiculoSchema,
    summary="Buscar veículo por placa",
    dependencies=[Depends(get_usuario_atual)]
)
async def buscar_veiculo(placa: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VeiculoModel).filter(VeiculoModel.Placa == placa)
        result = await session.execute(query)
        veiculo = result.scalar_one_or_none()
        if not veiculo:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        return veiculo


@router.delete(
    '/{placa}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir veículo",
    description="Remove um veículo pelo número de placa. Requer permissão de administrador.",
    dependencies=[Depends(exigir_admin)]
)
async def deletar_veiculo(placa: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VeiculoModel).filter(VeiculoModel.Placa == placa)
        result = await session.execute(query)
        veiculo = result.scalar_one_or_none()
        if not veiculo:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        await session.delete(veiculo)
        await session.commit()
