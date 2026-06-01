from sqlalchemy import Column, String, ForeignKey
from core.configs import DBBaseModel

class VeiculoModel(DBBaseModel):
    __tablename__ = 'veiculos'
    
    Placa = Column(String(7), primary_key=True)
    Chassi = Column(String(20), unique=True, nullable=False)
    Modelo = Column(String(50))
    Marca = Column(String(50))
    Cor = Column(String(30))
    Situacao = Column(String(20), nullable=False)
    CPFProprietario = Column(String(14), ForeignKey('proprietarios.CPF'))