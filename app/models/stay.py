from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Stay(Base):
    __tablename__ = "stays"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True)
    actual_check_in = Column(DateTime, default=datetime.utcnow)
    actual_check_out = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)

    booking = relationship("Booking", back_populates="stay")