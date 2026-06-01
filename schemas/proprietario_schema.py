from typing import Optional
from pydantic import BaseModel, Field

class ProprietarioSchema(BaseModel):
    CPF: str = Field(..., min_length=11, max_length=14)
    Nome: str = Field(..., max_length=100)
    
    class Config:
        from_attributes = True