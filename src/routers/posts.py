from typing import List
from fastapi import APIRouter, Depends
from src.controllers.current_user import get_current_user
from src.model.core import User
from src.model.schemas import PostReponce
from src.controllers.get_user_posts import get_user_posts, get_user_post, delete_user_post
from src.database import get_async_session
from src.controllers.get_all_posts import get_all_posts
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache


router = APIRouter()


@router.get('/posts')
async def fetch_user_posts(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_session)):
    return await get_user_posts(current_user, db)


@router.get('/posts/all', response_model=List[PostReponce])
@cache(expire=30)
async def fetch_all_posts(db: AsyncSession = Depends(get_async_session)):
    posts = await get_all_posts(db)
    return posts


@router.get('/posts/{id}')
@cache(expire=30)
async def fetch_user_post(id: int, db: AsyncSession = Depends(get_async_session)):
    return await get_user_post(id, db)


@router.get('/posts/delete/{id}')
async def delete_post(id: int, db: AsyncSession = Depends(get_async_session)):
    await delete_user_post(id, db)
    return {'status': "ok"}
