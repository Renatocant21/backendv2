from typing import Optional
from datetime import date
from pydantic import BaseModel


class RelatorioCriarSchema(BaseModel):
    idUsuario: int
    Data: date
    Descricao: Optional[str] = None


class RelatorioSchema(BaseModel):
    idRelatorio: Optional[int] = None
    idUsuario: int
    Data: date
    Descricao: Optional[str] = None

    class Config:
        from_attributes = True
