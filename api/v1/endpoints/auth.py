from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session
from pydantic import BaseModel

router = APIRouter()

class LoginData(BaseModel):
    email: str
    senha: str

@router.post('/login')
async def login(dados: LoginData, db: AsyncSession = Depends(get_session)):
    return {"access_token": "fake-token-para-teste", "token_type": "bearer"}

@router.post('/logout')
async def logout():
    return {"detail": "Logout realizado"}

@router.get('/acessos')
async def listar_acessos():
    return []
