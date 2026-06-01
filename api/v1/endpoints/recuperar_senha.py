import secrets
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session
from core.security import hash_senha
from models.usuario_model import UsuarioModel
from models.recuperar_senha_model import RecuperarSenhaModel
from schemas.recuperar_senha_schema import (
    RecuperarSenhaSolicitarSchema,
    RecuperarSenhaConfirmarSchema,
    RecuperarSenhaSchema,
)

router = APIRouter()


@router.post(
    "/solicitar",
    status_code=status.HTTP_200_OK,
    summary="Solicitar recuperação de senha",
    description=(
        "Recebe o e-mail do usuário e gera um token de recuperação. "
        "Em produção, esse token seria enviado por e-mail; aqui ele é retornado "
        "diretamente para facilitar os testes via Swagger."
    )
)
async def solicitar_recuperacao(
    dados: RecuperarSenhaSolicitarSchema,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        result = await session.execute(
            select(UsuarioModel).filter(UsuarioModel.email == dados.email)
        )
        usuario = result.scalar_one_or_none()

    if not usuario:
        # Resposta genérica para não revelar se o e-mail existe
        return {"detail": "Se o e-mail estiver cadastrado, você receberá as instruções."}

    token = secrets.token_hex(32)  # 64 caracteres hex

    nova_recuperacao = RecuperarSenhaModel(
        idUsuario=usuario.idUsuario,
        token=token,
        dataSolicitacao=date.today()
    )

    async with db as session:
        session.add(nova_recuperacao)
        await session.commit()

    # Em produção: enviar por e-mail. Aqui retornamos para fins de teste.
    return {
        "detail": "Token gerado com sucesso.",
        "token": token  # Remover em produção — enviar por e-mail
    }


@router.post(
    "/confirmar",
    status_code=status.HTTP_200_OK,
    summary="Confirmar nova senha com token",
    description="Recebe o token de recuperação e a nova senha, e atualiza a senha do usuário."
)
async def confirmar_recuperacao(
    dados: RecuperarSenhaConfirmarSchema,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        result = await session.execute(
            select(RecuperarSenhaModel).filter(RecuperarSenhaModel.token == dados.token)
        )
        recuperacao = result.scalar_one_or_none()

    if not recuperacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado."
        )

    async with db as session:
        result = await session.execute(
            select(UsuarioModel).filter(UsuarioModel.idUsuario == recuperacao.idUsuario)
        )
        usuario = result.scalar_one_or_none()

        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

        usuario.Senha = hash_senha(dados.nova_senha)

        # Remove o token após uso
        recuperacao_obj = await session.get(RecuperarSenhaModel, recuperacao.idRecuperacao)
        if recuperacao_obj:
            await session.delete(recuperacao_obj)

        await session.commit()

    return {"detail": "Senha atualizada com sucesso."}


@router.get(
    "/",
    response_model=list[RecuperarSenhaSchema],
    summary="Listar solicitações de recuperação (admin)",
    description="Lista todas as solicitações de recuperação de senha em aberto."
)
async def listar_recuperacoes(
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        result = await session.execute(select(RecuperarSenhaModel))
        return result.scalars().all()

