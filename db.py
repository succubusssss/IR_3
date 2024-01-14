from config import settings
from sqlalchemy import insert, select
from sqlalchemy import create_engine, text
from models.good import Base, User
#ur_p = "postgresql+asyncpg://postgres:nbnfybr911@localhost:5432/base_3"
#engine = create_async_engine(ur_p, echo=True)
ur_s = settings.POSTGRES_DATABASE_URLS
ur_a = settings.POSTGRES_DATABASE_URLA

print(ur_s)

#engine_a = create_async_engine(ur_a, echo=True)
engine_s = create_engine(ur_s, echo=True)

def create_tables():
    #Base.metadata.drop_all(bind=engine_s)
    Base.metadata.create_all(bind=engine_s)
    #Base.metadata
create_tables()

def f():
    with engine_s.connect() as conn:
        answer = conn.execute(text("select * from users;"))
        print(f"answer={answer.all()}")
#asyncio.run(f())

def f_bilder():
    with engine_s.begin() as conn:
        query = insert(User).values(
            [{"name": "Юдина Анна Гагиковна 404б", "hashed_password":"404б"},
             {"name": "Сидоркин", "hashed_password":"12345"},
             {"name": "Oркин", "hashed_password":"145d556"}])
        conn.execute(query)
        conn.execute(text('commit;'))
        query = select(User)
        answer = conn.execute(query)
        print(f"answer = {answer.all()}")
#f_bilder()