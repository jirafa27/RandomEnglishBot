from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.database import get_db
from sqlalchemy import select
from api.models import User

user_routes = APIRouter()


@user_routes.get("/{telegram_id}")
async def get_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.telegram_id == telegram_id)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        return {"error": "User not found"}

    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "language_level": user.language_level,
        "is_premium": user.is_premium,
        "created_at": user.created_at,
    }
