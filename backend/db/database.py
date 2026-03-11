from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from core.config import settings

# 1. The Model Base (Used by all models)
class Base(DeclarativeBase):
    pass

# 2. The Engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

# 3. The Session Factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
