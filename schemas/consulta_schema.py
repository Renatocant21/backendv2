from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ConsultaSchema(BaseModel):
    idConsulta: int
    Placa: str
    idUsuario: int
    tipoConsulta: str
    dataHora: datetime
    Resultado: Optional[str] = None
    
    class Config:
        from_attributes = True