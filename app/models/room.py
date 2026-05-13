from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)
    type = Column(String) # single, double, suite
    price_per_night = Column(Float)
    status = Column(String, default="available") # available, occupied, cleaning
    floor = Column(Integer)
    description = Column(String, nullable=True)

    # Используем строки для связи, чтобы избежать циклических импортов
    bookings = relationship("Booking", back_populates="room")
    cleaning_tasks = relationship("CleaningTask", back_populates="room")