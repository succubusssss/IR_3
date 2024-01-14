from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from models.good import *
from sqlalchemy.orm import sessionmaker, Session
from db import engine_s
from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import JSONResponse, Response
from models.good import New_Respons, Tags
# nest_asyncio.apply()
#user_router = APIRouter(tags=[Tags.users])

#
# #def init_db():
# #   Base.metadata.create_all(bind=engine_s)
#
# async def init_db():
#     async with engine_a.begin() as conn:
#         await conn.run.sync(Base.metadata.create_all)
# session_make = sessionmaker(engine_a)
# async def get_async_session():
#     async with Session(engine_a) as session:
#         try:
#             yield session
#         finally:
#             session.close()
session_make = sessionmaker(engine_s)
def get_session():
    with Session(engine_s) as session:
        try:
            yield session
        finally:
            session.close()

#реализация маршрутов для операций с конкретными тегами - конкретизация роутера
users_router=APIRouter(tags=[Tags.users], prefix='/api/users')
info_router=APIRouter(tags=[Tags.info])

def coder_passwd(cod: str):
    return cod*2

@users_router.get("/{id}", response_model=Union[New_Respons, Main_User], tags=[Tags.info])
def get_user_(id: int, DB: Session = Depends(get_session)):
    #Ищем пользователя по id
    user=DB.query(User).filter(User.id == id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message":"Пользователь не найден"})
    else:
        return user

@users_router.get("/", response_model=Union[list[Main_User],New_Respons], tags=[Tags.info])
def get_users_db(DB: Session = Depends(get_session)):
    #Получаем все записи
    user=DB.query(User).all()
    if user == None:
        return JSONResponse(status_code=404, content={"message":"Пользователь не найден"})
    else:
        return user
@users_router.post("/", response_model=Union[Main_User, New_Respons], tags=[Tags.users], status_code=status.HTTP_201_CREATED)
def create_user(item: Annotated[Main_User, Body(embed=True, description="Новый пользователь")],
                DB:Session=Depends(get_session)):
    try:
        user=User(name=item.name, hashed_password=coder_passwd(item.name))
        if user is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(user)
        DB.commit()
        DB.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Произошла ошибка при добавлении объекта {user}")
@users_router.delete("/{id}", response_class=JSONResponse, tags=[Tags.users])
def delete_user(id: int, DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        DB.delete(user)
        DB.commit()
    except HTTPException:
        JSONResponse(content={"message": f"Ошибка"})
    return JSONResponse(content={"message": f"Пользователь удалён {id}"})

@users_router.put("/", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
def edit_user_(item: Annotated[Main_User, Body(embed=True, description="Изменяем данные пользователя по id")],
               DB:Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == item.id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    user.name = item.name
    try:
        DB.commit()
        DB.refresh(user)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})
    return user

@users_router.patch("/{id}", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
def edit_user_plus(item: Annotated[Main_User,
Body(embed=True, description="Изменяем данные по id")], DB: Session = Depends(get_session)):
    # получаем пользователя по id
    try:
        user = DB.query(User).filter(User.id == item.id).first() #нашли элемент по ключу
        if user == None:
            return New_Respons(message="ошибка")
        user_dict = item.dict(exclude_unset=True) #преобразуем объект модели в словарь, но только только те данные,
        # которые были установлены (отправлены в запросе), без значений по умолчанию (данные для изменения в удобный формат)
        user_model = User(**user_dict)
        DB.commit()
        return user_model
    except HTTPException:
        return New_Respons(message = f'Ошибка {Response.status_code}')






