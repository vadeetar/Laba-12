from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.guest import Guest
from app.schemas import GuestCreate


class GuestService:
    @staticmethod
    def create_guest(db: Session, guest_data: GuestCreate):
        db_guest = db.query(Guest).filter(
            (Guest.email == guest_data.email) |
            (Guest.passport_number == guest_data.passport_number)
        ).first()
        if db_guest:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Гость с таким email или паспортом уже существует"
            )

        new_guest = Guest(**guest_data.model_dump())
        db.add(new_guest)
        db.commit()
        db.refresh(new_guest)
        return new_guest

    @staticmethod
    def get_all_guests(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Guest).offset(skip).limit(limit).all()