from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.core import User


async def get_user(id: int, session: AsyncSession):
    result = await session.execute(
        select(User).filter(User.id == id)
    )
    user = result.scalars().first()
    return user
