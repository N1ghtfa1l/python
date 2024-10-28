from src.model.schemas import UserUpdateDescription
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.core import User
from fastapi import HTTPException


async def update_description(
    user_id: int,
    update_data: UserUpdateDescription,
    db: AsyncSession,
):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.description = update_data.description
    await db.commit()
    await db.refresh(user)
    return user
