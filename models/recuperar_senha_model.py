from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel


class RecuperarSenhaModel(DBBaseModel):
    __tablename__ = 'RecuperarSenha'

    idRecuperacao = Column(Integer, primary_key=True)
    idUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'), nullable=False)
    token = Column(String(64), nullable=False)
    dataSolicitacao = Column(Date, nullable=False)

    usuario = relationship('UsuarioModel', backref='recuperacoes_senha')
