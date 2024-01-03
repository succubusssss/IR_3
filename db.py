import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_session
from sqlalchemy import create_engine, text

ur_p = "postgresql+asyncpg://postgres:nbnfybr911@localhost:5432/base_3"
#engine = create_engine(ur_p, echo=True)
engine=create_async_engine(ur_p, echo=True)
async def f():
    async with engine.begin() as conn:
        answer = await conn.execute(text("select version()"))
        print(f"answer={answer.all()}")
asyncio.run(f())