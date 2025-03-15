from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://user:password@localhost/englishclub"
)

# Создаём асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаём асинхронную фабрику сессий
AsyncSessionLocal = sessionmaker(
    engine,  # Передаём движок
    class_=AsyncSession,  # Указываем класс сессии
    expire_on_commit=False,  # Сессия не сбрасывается после коммита
)


# Dependency для FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
