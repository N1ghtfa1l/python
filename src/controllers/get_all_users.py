from sqlalchemy import select
from src.model.core import User
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users