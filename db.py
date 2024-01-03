import asyncio
from config import settings
from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_session
from sqlalchemy import create_engine, text
from models.good import Base
from sqlalchemy.orm import declarative_base

#ur_p = "postgresql+asyncpg://postgres:nbnfybr911@localhost:5432/base_3"
#engine = create_engine(ur_p, echo=True)
ur_s = settings.POSTGRES_DATABASE_URLS
ur_a = settings.POSTGRES_DATABASE_URLA

print(ur_s)

engine_a = create_async_engine(ur_a, echo=True)
engine_s = create_engine(ur_s, echo=True)

def create_tables():
    Base.metadata.drop_all(bind=engine_s)
    Base.metadata.create_all(bind=engine_s)
    #Base.metadata


def f():
    with engine_s.connect() as conn:
        answer = conn.execute(text("select * from users:"))
        print(f"answer={answer.all()}")
#asyncio.run(f())