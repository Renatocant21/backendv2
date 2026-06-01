from pydantic import BaseModel, Field

class RestricaoSchema(BaseModel):
    Placa: str = Field(..., min_length=7, max_length=7)
    tipoRestricao: str
    
    class Config:
        from_attributes = True