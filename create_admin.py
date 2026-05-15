from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash


def create_first_admin():
    db = SessionLocal()

    # Проверяем, есть ли уже такой пользователь
    existing_user = db.query(User).filter(User.username == "admin").first()
    if existing_user:
        print("Пользователь 'admin' уже существует.")
        db.close()
        return

    # Создаем админа
    hashed_pwd = get_password_hash("admin123")
    admin_user = User(
        username="admin",
        email="admin@hotel.com",
        hashed_password=hashed_pwd,
        role="admin",
        is_active=True
    )

    db.add(admin_user)
    db.commit()
    print("✅ Администратор успешно создан! Логин: admin | Пароль: admin123")
    db.close()


if __name__ == "__main__":
    create_first_admin()