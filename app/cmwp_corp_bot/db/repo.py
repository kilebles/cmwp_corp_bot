from contextlib import asynccontextmanager

from app.cmwp_corp_bot.db.session import AsyncSessionLocal


@asynccontextmanager
async def get_session():
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise
    finally:
        await session.close()