from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session
from core.security import verificar_senha, criar_token_acesso
from models.usuario_model import UsuarioModel
from models.acesso_model import AcessoModel
from schemas.auth_schema import TokenSchema
from schemas.acesso_schema import AcessoSchema

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenSchema,
    summary="Autenticação de usuário",
    description="Recebe login e senha, retorna JWT Bearer token e registra o acesso."
)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.Login == form.username)
        result = await session.execute(query)
        usuario = result.scalar_one_or_none()

        if not usuario or not verificar_senha(form.password, usuario.Senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Login ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Registra o acesso (login)
        novo_acesso = AcessoModel(
            idUsuario=usuario.idUsuario,
            dataHoraLogin=date.today(),
            dataHoraLogout=None
        )
        session.add(novo_acesso)
        await session.commit()
        await session.refresh(novo_acesso)

    token = criar_token_acesso({
        "sub": usuario.Login,
        "tipo": usuario.tipoUsuario,
        "acesso_id": novo_acesso.idAcesso
    })
    return {"access_token": token, "token_type": "bearer"}


@router.post(
    "/logout",
    summary="Logout do usuário",
    description="Registra o horário de logout do usuário autenticado."
)
async def logout(
    db: AsyncSession = Depends(get_session),
    usuario_atual=Depends(get_usuario_atual)
):
    async with db as session:
        # Busca o último acesso sem logout deste usuário
        result = await session.execute(
            select(AcessoModel)
            .filter(
                AcessoModel.idUsuario == usuario_atual.idUsuario,
                AcessoModel.dataHoraLogout == None
            )
            .order_by(AcessoModel.idAcesso.desc())
        )
        acesso = result.scalars().first()

        if acesso:
            acesso.dataHoraLogout = date.today()
            await session.commit()

    return {"detail": "Logout registrado com sucesso"}


@router.get(
    "/acessos",
    response_model=list[AcessoSchema],
    summary="Listar histórico de acessos",
    description="Retorna o histórico de logins/logouts. Requer autenticação."
)
async def listar_acessos(
    db: AsyncSession = Depends(get_session),
    usuario_atual=Depends(get_usuario_atual)
):
    async with db as session:
        result = await session.execute(select(AcessoModel))
        return result.scalars().all()

