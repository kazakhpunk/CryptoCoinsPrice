from pathlib import Path

import redis.asyncio as aioredis
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import Base, async_engine, get_async_db
from auth.auth import router as auth_router
from app.routers.external import router as external_router
from app.routers.local import router as local_router

load_dotenv(Path(__file__).parent.parent / '.env')

app = FastAPI()


redis_client = aioredis.from_url(settings.redis_url)


@app.on_event("startup")
async def startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "This is a FastAPI app that uses CoinGecko API"}


@app.get("/health")
async def check_health(db: AsyncSession = Depends(get_async_db)):
    try:
        await db.execute(text("SELECT 1"))
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        await redis_client.ping()
    except (aioredis.ConnectionError, aioredis.TimeoutError):
        raise HTTPException(status_code=500, detail="Redis connection failed")

    return {"status": "ok", "database": "connected", "redis": "connected"}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(external_router, prefix="/external", tags=["external"])
app.include_router(local_router, prefix="/local", tags=["local"])
