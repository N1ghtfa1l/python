from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.core import User, Post


async def get_user_posts(current_user: User, session: AsyncSession):
    result = await session.execute(
        select(Post).filter(Post.user_id == current_user.id)
    )
    posts = result.scalars().all()
    return posts


async def get_user_post(id: int, session: AsyncSession):
    result = await session.execute(
        select(Post).filter(Post.user_id == id)
    )
    posts = result.scalars().all()
    return posts


async def delete_user_post(post_id: int, session: AsyncSession):
    result = await session.execute(
        select(Post).filter(Post.id == post_id)
    )
    post = result.scalars().first()

    if post:
        await session.delete(post)
        await session.commit()
