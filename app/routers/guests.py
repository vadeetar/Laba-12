from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import GuestCreate, GuestResponse
from app.services.guest_service import GuestService
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/guests", tags=["Guests"])

@router.post("/", response_model=GuestResponse, dependencies=[Depends(get_current_active_user)])
def create_guest(guest: GuestCreate, db: Session = Depends(get_db)):
    return GuestService.create_guest(db, guest)

@router.get("/", response_model=List[GuestResponse], dependencies=[Depends(get_current_active_user)])
def read_guests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return GuestService.get_all_guests(db, skip=skip, limit=limit)