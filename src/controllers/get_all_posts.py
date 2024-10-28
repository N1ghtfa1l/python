from sqlalchemy import select
from src.model.core import Post
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_posts(session: AsyncSession):
    result = await session.execute(select(Post))
    posts = result.scalars().all()
    return posts
