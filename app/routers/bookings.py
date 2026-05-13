from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import BookingCreate, BookingResponse, StayResponse
from app.services.booking_service import BookingService
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

# Обрати внимание: зависимость Depends(get_current_active_user) защищает эндпоинт,
# а booking: BookingCreate заставляет FastAPI читать JSON из тела запроса.
@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_user)])
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """Создает новое бронирование, проверяя пересечение дат"""
    return BookingService.create_booking(db, booking)

@router.post("/{booking_id}/checkin", response_model=StayResponse, dependencies=[Depends(get_current_active_user)])
def check_in(booking_id: int, db: Session = Depends(get_db)):
    """Заселяет гостя, меняет статус комнаты на occupied"""
    return BookingService.check_in_guest(db, booking_id)

@router.post("/stays/{stay_id}/checkout", dependencies=[Depends(get_current_active_user)])
def check_out(stay_id: int, db: Session = Depends(get_db)):
    """Выселяет гостя, завершает бронь и создает задачу на уборку"""
    return BookingService.check_out_guest(db, stay_id)