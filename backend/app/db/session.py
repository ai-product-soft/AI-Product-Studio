from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import settings

database_url = settings.DATABASE_URL
if database_url.startswith("postgresql+psycopg2"):
    database_url = database_url.replace("postgresql+psycopg2", "postgresql+asyncpg", 1)

engine = create_async_engine(
    database_url,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
