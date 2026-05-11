from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: datetime


class UsersData(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserLogin(CreateUser):
    pass
