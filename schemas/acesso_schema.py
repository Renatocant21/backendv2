from typing import Optional
from datetime import date
from pydantic import BaseModel


class AcessoSchema(BaseModel):
    idAcesso: Optional[int] = None
    idUsuario: int
    dataHoraLogin: date
    dataHoraLogout: Optional[date] = None

    class Config:
        from_attributes = True
