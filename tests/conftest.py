import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.core.security import get_password_hash

# Используем in-memory базу данных SQLite для быстрых и чистых тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Создает чистую базу данных для каждого теста, а затем удаляет ее."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Подменяет зависимость get_db в FastAPI на тестовую сессию."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
def admin_token_headers(client, db_session):
    """Создает админа и возвращает заголовки с JWT токеном для защиты роутов."""
    admin_user = User(
        username="admin_test",
        email="admin@test.com",
        hashed_password=get_password_hash("password123"),
        role="admin",
        is_active=True
    )
    db_session.add(admin_user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={"username": "admin_test", "password": "password123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}