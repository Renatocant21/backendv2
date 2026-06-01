from sqlalchemy import Column, String, ForeignKey
from core.configs import DBBaseModel

class RestricaoModel(DBBaseModel):
    __tablename__ = 'restricoes'
    
    Placa = Column(String(7), ForeignKey('veiculos.Placa'), primary_key=True)
    tipoRestricao = Column(String(20), nullable=False)