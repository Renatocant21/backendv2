import asyncio
from core.database import engine

async def testar():
    try:
        async with engine.connect() as conn:
            print("✅ Conexão bem sucedida!")
    except Exception as e:
        print(f"❌ Erro: {e}")

asyncio.run(testar())