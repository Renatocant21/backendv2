from fastapi import FastAPI
from core.configs import settings
from api.api import api_router

app = FastAPI(
    title='Sistema de Consulta de Placas - Roubo/Furto',
    description='API para consulta de veículos com restrição de roubo ou furto.',
    version='1.0.0',
    contact={"name": "Suporte", "email": "suporte@exemplo.com"},
    license_info={"name": "MIT"},
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
