# Hotel Management System

Полноценное FastAPI-приложение для лабораторной работы №12.

## Возможности

- JWT аутентификация
- CRUD для Room, Guest, Booking, Stay, CleaningTask
- Отчёты и аналитика
- Docker
- Alembic
- Pytest + coverage
- GitHub Actions

## Запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker

```bash
docker-compose up --build
```

## Swagger

http://localhost:8000/docs