🔗 Сервис сокращения ссылок

Асинхронный сервис на FastAPI: создавай короткие ссылки, получай статистику переходов.

🚀 Функционал

- POST `/shorten` — создать короткую ссылку
- GET `/{short_code}` — редирект на оригинал
- GET `/stats/{short_code}` — статистика переходов
- Автоматическая генерация уникальных кодов
- Счётчик кликов

🛠 Стек

- Python 3.11 + FastAPI
- PostgreSQL + SQLAlchemy (async)
- Redis (опционально)
- Docker + docker-compose
- Pytest + pytest-asyncio

📦 Быстрый старт

bash
git clone https://github.com/yourname/url-shortener.git
cd url-shortener
docker-compose up --build
