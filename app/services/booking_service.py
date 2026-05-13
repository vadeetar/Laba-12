from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException, status
from datetime import datetime

from app.models.booking import Booking
from app.models.room import Room
from app.models.stay import Stay
from app.models.cleaning_task import CleaningTask
from app.schemas import BookingCreate


class BookingService:
    @staticmethod
    def create_booking(db: Session, booking_data: BookingCreate):
        # 1. Проверяем, не занята ли комната на эти даты
        overlapping_booking = db.query(Booking).filter(
            Booking.room_id == booking_data.room_id,
            Booking.status.in_(["pending", "confirmed"]),
            or_(
                and_(Booking.check_in_date <= booking_data.check_out_date,
                     Booking.check_out_date >= booking_data.check_in_date)
            )
        ).first()

        if overlapping_booking:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Комната уже забронирована на эти даты"
            )

        # 2. Считаем итоговую цену
        room = db.query(Room).filter(Room.id == booking_data.room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail="Комната не найдена")

        days = (booking_data.check_out_date - booking_data.check_in_date).days
        if days <= 0:
            raise HTTPException(status_code=400, detail="Дата выезда должна быть позже даты заезда")

        total_price = room.price_per_night * days

        # 3. Создаем запись
        new_booking = Booking(
            **booking_data.model_dump(),
            total_price=total_price,
            status="confirmed"
        )
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking

    @staticmethod
    def check_in_guest(db: Session, booking_id: int):
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Бронирование не найдено")
        if booking.status != "confirmed":
            raise HTTPException(status_code=400, detail="Бронирование не подтверждено или уже завершено")

        # Меняем статус комнаты
        room = db.query(Room).filter(Room.id == booking.room_id).first()
        room.status = "occupied"

        # Создаем запись о фактическом проживании (Stay)
        stay = Stay(booking_id=booking.id, actual_check_in=datetime.utcnow())
        db.add(stay)
        db.commit()
        db.refresh(stay)
        return stay

    @staticmethod
    def check_out_guest(db: Session, stay_id: int):
        stay = db.query(Stay).filter(Stay.id == stay_id).first()
        if not stay or stay.actual_check_out is not None:
            raise HTTPException(status_code=400, detail="Запись о проживании не найдена или гость уже выехал")

        stay.actual_check_out = datetime.utcnow()

        # Завершаем бронь
        booking = db.query(Booking).filter(Booking.id == stay.booking_id).first()
        booking.status = "completed"

        # Освобождаем комнату и отправляем на уборку
        room = db.query(Room).filter(Room.id == booking.room_id).first()
        room.status = "cleaning"

        # Автоматически создаем задачу для персонала
        cleaning_task = CleaningTask(
            room_id=room.id,
            status="pending",
            notes="Автоматическая генерация после выезда гостя"
        )
        db.add(cleaning_task)
        db.commit()

        # Возвращаем dict, так как роутер не привязан к Pydantic-схеме для этого ответа
        return {"id": stay.id, "actual_check_in": stay.actual_check_in, "actual_check_out": stay.actual_check_out}