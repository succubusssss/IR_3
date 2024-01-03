from fastapi import APIRouter, Body
from models.good import Main_User, Main_UserDB, New_Respons
from typing import Union, Annotated

users_router = APIRouter()

def coder_passwd(cod: str):
    result = cod*2

users_list = [Main_UserDB(name='Ivanov', id=108, password='********'), Main_UserDB(name="Petrov", id=134, password="********")]

def find_user(id: int) -> Union[Main_UserDB, None]:
    for user in users_list:
        if user.id == id:
            return user
    return None

@users_router.get("/api/users", response_model=Union[list[Main_User], None])
def get_users():
    return users_list

@users_router.get("/api/users/{id}", response_model=Union[Main_User, New_Respons])
def get_user(id: int):
    user = find_user(id)
    print(user)
    if user == None:
        return New_Respons(message="Пользователь не найден")
    return userZ

@users_router.post("/api/users", response_model=Union[Main_User, New_Respons])
def create_user(item: Annotated[Main_User, Body(embed=True, description="Новый пользователь")]):
    user = Main_UserDB(name=item.name, id=item.id, password=coder_passwd(item.name))
    users_list.append(user)
    return user

@users_router.put("/api/users", response_model=Union[Main_User, New_Respons])
def edit_user(item: Annotated[Main_User, Body(embed=True, description="Изменяем данные для пользователя по id")]):
    user = find_user(item.id)
    if user == None:
        return New_Respons(message="Пользователь не найден")
    user.id = item.id
    user.name = item.name
    return user

@users_router.delete("/api/users/{id}", response_model=Union[list[Main_User], None])
def delete_person(id:int):
    user = find_user(id)
    if user == None:
        return New_Respons(message="Пользователь не найден")
    users_list.remove(user)
    return users_list