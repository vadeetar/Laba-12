from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.room import Room
from app.models.booking import Booking
from app.core.dependencies import get_current_admin

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/occupancy", dependencies=[Depends(get_current_admin)])
def get_occupancy_report(db: Session = Depends(get_db)):
    """Аналитика: Процент занятых номеров"""
    total_rooms = db.query(Room).count()
    occupied_rooms = db.query(Room).filter(Room.status == "occupied").count()
    rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0

    return {
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms,
        "occupancy_rate": round(rate, 2)
    }


@router.get("/revenue", dependencies=[Depends(get_current_admin)])
def get_revenue_report(db: Session = Depends(get_db)):
    """Аналитика: Выручка по завершенным бронированиям"""
    total_revenue = db.query(func.sum(Booking.total_price)).filter(
        Booking.status == "completed"
    ).scalar() or 0.0

    return {"total_revenue": total_revenue}