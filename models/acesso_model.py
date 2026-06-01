from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel


class AcessoModel(DBBaseModel):
    __tablename__ = 'Acesso'

    idAcesso = Column(Integer, primary_key=True)
    idUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'), nullable=False)
    dataHoraLogin = Column(Date, nullable=False)
    dataHoraLogout = Column(Date, nullable=True)

    usuario = relationship('UsuarioModel', backref='acessos')
