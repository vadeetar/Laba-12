from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.room import Room

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/")
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


@router.post("/")
def create_room(
    number: str,
    room_type: str,
    price: float,
    floor: int,
    db: Session = Depends(get_db)
):
    room = Room(
        number=number,
        type=room_type,
        price_per_night=price,
        floor=floor
    )

    db.add(room)
    db.commit()
    db.refresh(room)

    return room


@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(404, "Room not found")

    db.delete(room)
    db.commit()

    return {"message": "Deleted"}