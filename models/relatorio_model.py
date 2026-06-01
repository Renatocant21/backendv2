from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel


class RelatorioModel(DBBaseModel):
    __tablename__ = 'Relatorio'

    idRelatorio = Column(Integer, primary_key=True)
    idUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'), nullable=False)
    Data = Column(Date, nullable=False)
    Descricao = Column(String(200))

    usuario = relationship('UsuarioModel', backref='relatorios')
