from datetime import datetime
from pydantic import BaseModel

class OperacaoSchema(BaseModel):
    idOperacao: int
    idUsuario: int
    tipoOperacao: str
    dataHora: datetime
    
    class Config:
        from_attributes = True