from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base # Убедись, что путь к Base верный

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="staff") # admin или staff
    is_active = Column(Boolean, default=True)