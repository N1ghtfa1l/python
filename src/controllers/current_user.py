from fastapi import Depends, HTTPException, Request
import jwt
from fastapi.security import OAuth2PasswordBearer
from src.config import SECRET_KEY
from src.model.schemas import TokenData
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from sqlalchemy import select
from src.model.core import User


async def get_current_user(request: Request, session: AsyncSession = Depends(get_async_session)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Не удалось проверить токен",
    )
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
    result = await session.execute(select(User).where(User.email == token_data.email))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
