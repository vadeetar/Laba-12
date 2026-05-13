from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, bookings, guests, cleaning, reports, rooms

# В реальном проекте используется Alembic,
# но для старта генерируем таблицы напрямую, если их еще нет.
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hotel Management API",
    description="Система управления гостиницей (Вариант 18)",
    version="1.0.0"
)

# Подключение всех модулей (маршрутов)
app.include_router(auth.router)
app.include_router(guests.router)
app.include_router(bookings.router)
app.include_router(cleaning.router)
app.include_router(reports.router)
app.include_router(rooms.router) # Предполагается, что CRUD для Room у тебя уже есть

@app.get("/")
def root():
    return {"message": "Welcome to the Hotel Management API"}