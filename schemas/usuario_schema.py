from typing import Optional
from pydantic import BaseModel, EmailStr


class UsuarioCriarSchema(BaseModel):
    Nome: str
    Login: str
    Senha: str
    email: str
    tipoUsuario: str


class UsuarioSchema(BaseModel):
    idUsuario: Optional[int] = None
    Nome: str
    Login: str
    email: str
    tipoUsuario: str

    class Config:
        from_attributes = True
