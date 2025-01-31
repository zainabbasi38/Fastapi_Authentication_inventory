from sqlmodel import Field
from typing import Optional
from app.models.common import BaseModel

class User(BaseModel, table=True):
    __tablename__= "users"
    first_name : str
    last_name : str
    user_name : str = Field(unique=True, index=True)   #we write Field to define usernae and email is unique
    email : str = Field(unique=True, index=True)
    password : str