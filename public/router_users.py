from fastapi import APIRouter, Depends,Body, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from models.good import *
from sqlalchemy.orm import sessionmaker, Session
from public.db import engine_s

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
def get_users_(id: int, DB: Session = Depends(get_session)):
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

@users_router.put("/", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
def edit_user_(item: Annotated[Main_User, Body(embed=True, description="Изменяем данные пользователя по id")],
               DB:Session = Depends(get_session)):
    user=DB.query(User).filter(User.id == item.id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    user.name = item.name
    try:
        DB.commit()
        DB.refresh(user)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})
    return user

@users_router.delete("\{id}", response_class=JSONResponse, tags=[Tags.users])
def delete_user(id: int, DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == item.id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        DB.delete(user)
        DB.commit()
    except HTTPException:
        return JSONResponse(content={"message": f"Ошибка"})
    return JSONResponse(content={"message": f"Пользователь удалён {id}"})













