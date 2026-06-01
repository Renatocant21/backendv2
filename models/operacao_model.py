from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from core.configs import DBBaseModel

class OperacaoModel(DBBaseModel):
    __tablename__ = 'operacoes'
    
    idOperacao = Column(Integer, primary_key=True)
    idUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'))
    tipoOperacao = Column(String(100), nullable=False)
    dataHora = Column(DateTime, nullable=False)