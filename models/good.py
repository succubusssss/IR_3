from typing import Union, Annotated
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import Column, String, Integer, Sequence, Identity, Float, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base

from enum import Enum


"""class Main_User(BaseModel):
    name: Union[str, None] = None
    id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    
class Main_UserDB(Main_User):
    password: Annotated[Union[str, None], Field(max_length=200, min_length=8)] = None

class New_Respons(BaseModel):
    message: str
"""

Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(start=1), primary_key=True)
    name = Column(String, index=True, nullable=False)
    hashed_password = Column(String)