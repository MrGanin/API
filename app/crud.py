from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models import URL

async def create_url(db: AsyncSession, short_code: str, original_url: str) -> URL:
    db_url = URL(short_code=short_code, original_url=str(original_url))
    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    return db_url

async def get_url_by_code(db: AsyncSession, short_code: str) -> URL | None:
    result = await db.execute(select(URL).where(URL.short_code == short_code))
    return result.scalar_one_or_none()

async def increment_clicks(db: AsyncSession, short_code: str) -> None:
    await db.execute(
        update(URL).where(URL.short_code == short_code).values(clicks=URL.clicks + 1)
    )
    await db.commit()