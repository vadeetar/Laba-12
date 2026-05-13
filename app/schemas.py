from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime


# --- СХЕМЫ ПОЛЬЗОВАТЕЛЯ (USER) ---
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str = "staff"


class UserResponse(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# --- СХЕМЫ КОМНАТ (ROOM) ---
class RoomBase(BaseModel):
    number: str
    type: str  # single, double, suite
    price_per_night: float
    floor: int
    description: Optional[str] = None


class RoomCreate(RoomBase):
    pass


class RoomResponse(RoomBase):
    id: int
    status: str  # available, occupied, cleaning

    model_config = ConfigDict(from_attributes=True)


# --- СХЕМЫ ГОСТЕЙ (GUEST) ---
class GuestBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone: str
    passport_number: str


class GuestCreate(GuestBase):
    pass


class GuestResponse(GuestBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- СХЕМЫ БРОНИРОВАНИЯ (BOOKING) ---
class BookingBase(BaseModel):
    room_id: int
    guest_id: int
    check_in_date: date
    check_out_date: date


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: int
    total_price: float
    status: str  # pending, confirmed, cancelled, completed

    model_config = ConfigDict(from_attributes=True)


# --- СХЕМЫ ПРОЖИВАНИЯ (STAY) ---
class StayBase(BaseModel):
    booking_id: int
    notes: Optional[str] = None


class StayCreate(StayBase):
    pass


class StayResponse(StayBase):
    id: int
    actual_check_in: Optional[datetime]
    actual_check_out: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# --- СХЕМЫ УБОРКИ (CLEANING TASK) ---
class CleaningTaskBase(BaseModel):
    room_id: int
    assigned_to: Optional[str] = None
    notes: Optional[str] = None


class CleaningTaskCreate(CleaningTaskBase):
    pass


class CleaningTaskResponse(CleaningTaskBase):
    id: int
    status: str  # pending, in_progress, done

    model_config = ConfigDict(from_attributes=True)