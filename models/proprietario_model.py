from sqlalchemy import Column, String
from core.configs import DBBaseModel

class ProprietarioModel(DBBaseModel):
    __tablename__ = 'proprietarios'
    
    CPF = Column(String(14), primary_key=True)
    Nome = Column(String(100), nullable=False)