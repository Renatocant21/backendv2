from typing import Optional
from datetime import date
from pydantic import BaseModel


class RecuperarSenhaSolicitarSchema(BaseModel):
    email: str


class RecuperarSenhaConfirmarSchema(BaseModel):
    token: str
    nova_senha: str


class RecuperarSenhaSchema(BaseModel):
    idRecuperacao: Optional[int] = None
    idUsuario: int
    token: str
    dataSolicitacao: date

    class Config:
        from_attributes = True
