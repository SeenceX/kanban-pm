from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from config import settings


sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    #pool_size=5, #максимально кол-во подключения к БД
    #max_overflow=10, #дополнительное кол-во подключений
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
)

#with engine.connect() as conn:
#   res = conn.execute(text("SELECT VERSION()"))
#   print(f"{res.all=}")