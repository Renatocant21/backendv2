from sqlalchemy import Column, Integer, String
from core.configs import DBBaseModel

class UsuarioModel(DBBaseModel):
    __tablename__ = 'usuarios'
    
    idUsuario = Column(Integer, primary_key=True)
    Nome = Column(String(100), nullable=False)
    Login = Column(String(50), unique=True, nullable=False)
    Senha = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    tipoUsuario = Column(String(20), nullable=False)