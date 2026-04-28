import secrets
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, engine, Base
from app.crud import create_url, get_url_by_code, increment_clicks
from app.schemas import URLCreate, URLResponse
from app.config import settings

app = FastAPI(title="URL Shortener", description="Асинхронный сервис сокращения ссылок")


@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def generate_short_code(length: int = 6) -> str:
    return secrets.token_urlsafe(length)[:length]


@app.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
async def shorten_url(
        url_data: URLCreate,
        db: AsyncSession = Depends(get_db)
):
    short_code = generate_short_code()

    while await get_url_by_code(db, short_code):
        short_code = generate_short_code()

    db_url = await create_url(db, short_code, str(url_data.original_url))

    return URLResponse(
        original_url=db_url.original_url,
        short_code=db_url.short_code,
        short_url=f"{settings.BASE_URL}/{db_url.short_code}",
        clicks=db_url.clicks
    )


@app.get("/{short_code}")
async def redirect_to_original(
        short_code: str,
        db: AsyncSession = Depends(get_db)
):
    url_entry = await get_url_by_code(db, short_code)
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    await increment_clicks(db, short_code)
    return RedirectResponse(url=url_entry.original_url, status_code=307)


@app.get("/stats/{short_code}", response_model=URLResponse)
async def get_stats(
        short_code: str,
        db: AsyncSession = Depends(get_db)
):
    url_entry = await get_url_by_code(db, short_code)
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return URLResponse(
        original_url=url_entry.original_url,
        short_code=url_entry.short_code,
        short_url=f"{settings.BASE_URL}/{url_entry.short_code}",
        clicks=url_entry.clicks
    )