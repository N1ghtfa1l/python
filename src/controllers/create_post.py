
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.core import  User, Post
from src.model.schemas import PostData


async def create_post(post_data: PostData, db: AsyncSession, current_user: User):
    new_post = Post(
        name=post_data.name,
        description=post_data.description,
        user_id=current_user.id
    )
    db.add(new_post)
    await db.commit()
    return new_post
