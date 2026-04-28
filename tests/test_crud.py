import pytest
from app.crud import create_url, get_url_by_code, increment_clicks


@pytest.mark.asyncio
async def test_create_and_get_url(db_session):
    url = await create_url(db_session, "abc123", "https://crud-test.com")

    fetched = await get_url_by_code(db_session, "abc123")
    assert fetched is not None
    assert fetched.original_url == "https://crud-test.com"
    assert fetched.clicks == 0


@pytest.mark.asyncio
async def test_increment_clicks(db_session):
    await create_url(db_session, "test123", "https://clicks-test.com")

    await increment_clicks(db_session, "test123")
    url = await get_url_by_code(db_session, "test123")
    assert url.clicks == 1

    await increment_clicks(db_session, "test123")
    url = await get_url_by_code(db_session, "test123")
    assert url.clicks == 2


@pytest.mark.asyncio
async def test_get_nonexistent_url(db_session):
    result = await get_url_by_code(db_session, "no-such-code")
    assert result is None