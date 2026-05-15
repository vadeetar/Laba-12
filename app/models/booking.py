from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    guest_id = Column(Integer, ForeignKey("guests.id"))
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    status = Column(String, default="pending") # pending, confirmed, cancelled, completed
    total_price = Column(Float)

    room = relationship("Room", back_populates="bookings")
    guest = relationship("Guest", back_populates="bookings")
    stay = relationship("Stay", back_populates="booking", uselist=False)