import asyncpg
from app.config import settings


DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

pool = None


async def create_pool():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)


async def get_pool():
    return pool