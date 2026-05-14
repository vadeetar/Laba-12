from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.stay import Stay
from app.models.room import Room
from app.models.cleaning_task import CleaningTask


def create_stay_from_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        return None

    # Заменяем utcnow() на современный стандарт
    stay = Stay(
        booking_id=booking.id,
        actual_check_in=datetime.now(timezone.utc)
    )

    # Обновляем статус комнаты
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if room:
        room.status = "occupied"

    db.add(stay)
    db.commit()
    db.refresh(stay)
    return stay


def checkout_guest(db: Session, stay_id: int):
    stay = db.query(Stay).filter(Stay.id == stay_id).first()
    if not stay:
        return None

    # Фиксим время выезда
    stay.actual_check_out = datetime.now(timezone.utc)

    # Направляем комнату на уборку
    booking = db.query(Booking).filter(Booking.id == stay.booking_id).first()
    if booking:
        room = db.query(Room).filter(Room.id == booking.room_id).first()
        if room:
            room.status = "cleaning"
            # Автоматическое создание задачи на уборку
            new_task = CleaningTask(room_id=room.id, status="pending")
            db.add(new_task)

    db.commit()
    db.refresh(stay)
    return stay