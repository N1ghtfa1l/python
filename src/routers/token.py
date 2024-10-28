from fastapi import HTTPException
from fastapi import APIRouter, Depends, HTTPException
from src.model import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from sqlalchemy.future import select
from src.model.core import User
from passlib.context import CryptContext
from src.controllers.create_token import create_access_token
from fastapi import Response
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("", status_code=201)
async def user_auth(auth: schemas.UserAuth, response: Response, session: AsyncSession = Depends(get_async_session)):
    try:
        existing_user = await session.scalar(select(User).where(User.email == auth.email))

        if not existing_user:
            raise HTTPException(
                status_code=404, detail="Пользователь не найден!")

        if not pwd_context.verify(auth.password, existing_user.hashed_password):
            raise HTTPException(
                status_code=400, detail="Неправильный пароль или логин")

        access_token = create_access_token(data={"sub": existing_user.email})
        response.set_cookie(key="access_token",
                            value=access_token, httponly=False, secure=True, max_age=3600, samesite='none')

        return {
            "name": existing_user.name,
            "email": existing_user.email,
            "id": existing_user.id
        }
    except Exception as e:
        return e
