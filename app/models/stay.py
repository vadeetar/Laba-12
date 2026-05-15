from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base

class Stay(Base):
    __tablename__ = "stays"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    # Заменили устаревший utcnow на современный формат
    actual_check_in = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    actual_check_out = Column(DateTime, nullable=True)

    booking = relationship("Booking")