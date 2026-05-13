from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Путь к твоей базе данных SQLite (файл hotel.db в корне проекта)
SQLALCHEMY_DATABASE_URL = "sqlite:///./hotel.db"

# connect_args={"check_same_thread": False} нужен только для SQLite в FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency (зависимость), которую мы передаем в каждый эндпоинт для работы с БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()