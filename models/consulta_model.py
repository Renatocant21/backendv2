from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from core.configs import DBBaseModel

class ConsultaModel(DBBaseModel):
    __tablename__ = 'consultas'
    
    idConsulta = Column(Integer, primary_key=True)
    Placa = Column(String(7), ForeignKey('veiculos.Placa'))
    idUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'))
    tipoConsulta = Column(String(20), nullable=False)
    dataHora = Column(DateTime, nullable=False)
    Resultado = Column(String(100))