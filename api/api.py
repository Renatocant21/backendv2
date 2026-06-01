from fastapi import APIRouter
from api.v1.endpoints import (
    proprietario, veiculo, usuario, consulta,
    restricao, operacao, auth, relatorio, recuperar_senha
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix='/auth', tags=['autenticacao'])
api_router.include_router(usuario.router, prefix='/usuarios', tags=['usuarios'])
api_router.include_router(proprietario.router, prefix='/proprietarios', tags=['proprietarios'])
api_router.include_router(veiculo.router, prefix='/veiculos', tags=['veiculos'])
api_router.include_router(consulta.router, prefix='/consultas', tags=['consultas'])
api_router.include_router(restricao.router, prefix='/restricoes', tags=['restricoes'])
api_router.include_router(operacao.router, prefix='/operacoes', tags=['operacoes'])
api_router.include_router(relatorio.router, prefix='/relatorios', tags=['relatorios'])
api_router.include_router(recuperar_senha.router, prefix='/recuperar-senha', tags=['recuperar-senha'])
