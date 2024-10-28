from fastapi import Depends, APIRouter
from src.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.core import User
from src.controllers.create_post import create_post
from src.controllers.current_user import get_current_user
from src.model.schemas import PostData

router = APIRouter()


@router.post('/post', response_model=PostData, status_code=200)
async def create_post_route(posta_data: PostData, db: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    return await create_post(posta_data, db, current_user)
