from fastapi import FastAPI
from core.configs import settings
from api.api import api_router
from sqlalchemy import create_engine, text
import os

app = FastAPI(
    title='Sistema de Consulta de Placas - Roubo/Furto',
    description='API para consulta de veículos com restrição de roubo ou furto.',
    version='1.0.0',
    contact={"name": "Suporte", "email": "suporte@exemplo.com"},
    license_info={"name": "MIT"},
)

# ========== ENDPOINTS DE DIAGNÓSTICO ==========

@app.get("/health")
async def health_check():
    return {"status": "ok", "api_version": "1.0.0"}

@app.get("/check-db")
async def check_database():
    try:
        sync_url = os.getenv("DATABASE_URL")
        if not sync_url:
            return {"error": "DATABASE_URL não encontrada"}
        
        engine = create_engine(sync_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            db_ok = result.scalar() == 1
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public'"))
            tables = [row[0] for row in result.fetchall()]
        
        engine.dispose()
        
        return {
            "db_conectado": db_ok,
            "tabelas_existentes": tables,
            "tabela_proprietario_existe": "proprietario" in tables or "proprietariomodel" in tables
        }
    except Exception as e:
        return {"error": str(e), "tipo": type(e).__name__}

@app.post("/init-db")
async def init_database():
    try:
        from models.proprietario_model import ProprietarioModel
        from core.database import Base
        
        sync_url = os.getenv("DATABASE_URL")
        engine = create_engine(sync_url)
        Base.metadata.create_all(bind=engine)
        engine.dispose()
        
        return {"message": "Tabelas criadas/verificadas com sucesso"}
    except Exception as e:
        return {"error": str(e)}

# ========== ROTAS PRINCIPAIS ==========

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)