import email
from typing import List
from pydantic import BaseModel, EmailStr


from app.schemas.article import Article


class UserBase(BaseModel):
    email: EmailStr
    is_admin: bool


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    articles: List[Article] = []

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str