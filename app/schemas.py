from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserBack(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostsBack(Post):
    id:int
    created_at: datetime 
    user_id: int
    owner: UserBack

    class Config:
        orm_mode = True



