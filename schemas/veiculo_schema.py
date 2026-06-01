from typing import Optional
from pydantic import BaseModel, Field

class VeiculoSchema(BaseModel):
    Placa: str = Field(..., min_length=7, max_length=7)
    Chassi: str = Field(..., min_length=17, max_length=20)
    Modelo: Optional[str] = None
    Marca: Optional[str] = None
    Cor: Optional[str] = None
    Situacao: str
    CPFProprietario: str
    
    class Config:
        from_attributes = True

class ConsultaPlacaResponse(BaseModel):
    Placa: str
    Situacao: str
    Mensagem: str
    Proprietario: str
    Modelo: str
    Marca: str
    Cor: str