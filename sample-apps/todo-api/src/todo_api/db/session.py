from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from todo_api.config import settings

# Create async engine according to the settings
engine = create_async_engine(settings.DATABASE_URL, echo=settings.SQL_ECHO, future=True)

# Create session factory
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for database session.

    Yields:
        AsyncSession: The database session.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
