from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.stay import Stay
from app.models.room import Room
from app.models.cleaning_task import CleaningTask

class BookingService:
    @staticmethod
    def create_booking(db: Session, booking_data):
        new_booking = Booking(**booking_data.model_dump())
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking

    @staticmethod
    def check_in_guest(db: Session, booking_id: int):
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return None
        stay = Stay(booking_id=booking.id, actual_check_in=datetime.now(timezone.utc))
        room = db.query(Room).filter(Room.id == booking.room_id).first()
        if room:
            room.status = "occupied"
        db.add(stay)
        db.commit()
        db.refresh(stay)
        return stay

    @staticmethod
    def check_out_guest(db: Session, stay_id: int):
        stay = db.query(Stay).filter(Stay.id == stay_id).first()
        if not stay:
            return None
        stay.actual_check_out = datetime.now(timezone.utc)
        booking = db.query(Booking).filter(Booking.id == stay.booking_id).first()
        if booking:
            room = db.query(Room).filter(Room.id == booking.room_id).first()
            if room:
                room.status = "cleaning"
                new_task = CleaningTask(room_id=room.id, status="pending")
                db.add(new_task)
        db.commit()
        db.refresh(stay)
        return stay