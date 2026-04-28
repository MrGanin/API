import pytest
from app.crud import create_url


@pytest.mark.asyncio
async def test_create_short_url(client):
    response = await client.post(
        "/shorten",
        json={"original_url": "https://example.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert "short_url" in data
    assert data["clicks"] == 0
    assert data["original_url"] == "https://example.com"


@pytest.mark.asyncio
async def test_redirect_to_original(client):
    # Сначала создаём ссылку
    create_response = await client.post(
        "/shorten",
        json={"original_url": "https://google.com"}
    )
    short_code = create_response.json()["short_code"]

    # Теперь редирект
    redirect_response = await client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://google.com"


@pytest.mark.asyncio
async def test_redirect_404(client):
    response = await client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Short URL not found"


@pytest.mark.asyncio
async def test_stats_endpoint(client):
    create_response = await client.post(
        "/shorten",
        json={"original_url": "https://stats-test.com"}
    )
    short_code = create_response.json()["short_code"]

    # Переходим 2 раза
    await client.get(f"/{short_code}")
    await client.get(f"/{short_code}")

    # Проверяем статистику
    stats_response = await client.get(f"/stats/{short_code}")
    assert stats_response.status_code == 200
    assert stats_response.json()["clicks"] == 2


@pytest.mark.asyncio
async def test_invalid_url_validation(client):
    response = await client.post(
        "/shorten",
        json={"original_url": "not-a-valid-url"}
    )
    assert response.status_code == 422  # Pydantic validation error


@pytest.mark.asyncio
async def test_unique_short_codes(client):
    # Создаём две одинаковые ссылки — коды должны быть разными
    resp1 = await client.post("/shorten", json={"original_url": "https://same.com"})
    resp2 = await client.post("/shorten", json={"original_url": "https://same.com"})

    code1 = resp1.json()["short_code"]
    code2 = resp2.json()["short_code"]

    assert code1 != code2