import asyncio
import uvicorn
from core.db.create_db import create_db
from fastapi import FastAPI
from routers import router
from settings import settings

app = FastAPI(debug=settings.SERVER_TEST)
app.include_router(router)


async def main():
    await create_db()
    uvicorn.run(
        "main:app",
        host=settings.SERVER_ADDR,
        port=settings.SERVER_PORT,
        reload=settings.SERVER_TEST,
        log_level="debug" if settings.SERVER_TEST else "info",
    )


if __name__ == "__main__":
    asyncio.run(main())
