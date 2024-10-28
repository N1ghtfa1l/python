from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from src.model import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from sqlalchemy.future import select
from src.model.core import User
from src.model.schemas import UserResponse, UserUpdateDescription
from passlib.context import CryptContext
from src.controllers.current_user import get_current_user
from src.controllers.get_all_users import get_all_users
from src.controllers.get_user import get_user
from src.controllers.update_user_desc import update_description
from fastapi_cache.decorator import cache

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(register: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    existing_user = await session.scalar(select(User).where(User.email == register.email))
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email уже есть!"
        )
    user = User(
        email=register.email,
        name=register.name,
        hashed_password=pwd_context.hash(register.password),
        is_active=True,
        role="User"
    )
    session.add(user)
    await session.commit()
    return user


@router.get("/auth")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"message": "ok"}


@router.get("/all", response_model=List[UserResponse])
async def fetch_all_users(db: AsyncSession = Depends(get_async_session)):
    result = await get_all_users(db)
    return result


@router.get('/one/{id}', response_model=UserResponse)
async def get_one_user(id: int, db: AsyncSession = Depends(get_async_session)):
    user = await get_user(id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put('/update/{user_id}')
async def update_user_desc(
    user_id: int,
    update_data: UserUpdateDescription = Body(...),
    db: AsyncSession = Depends(get_async_session)
):
    return await update_description(user_id, update_data, db)
