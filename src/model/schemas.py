from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    name: str


UserAuth = UserCreate


class TokenData(BaseModel):
    email: EmailStr

class PostReponce(BaseModel):
    name: str
    description: str
    user_id: int


class PostData(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    name: str
    id: int
    description: Optional[str] = None

class UserUpdateDescription(BaseModel):
    description: str
