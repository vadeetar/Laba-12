from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import CleaningTaskResponse
from app.services.cleaning_service import CleaningService
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/cleaning", tags=["Cleaning Tasks"])

@router.get("/", response_model=List[CleaningTaskResponse], dependencies=[Depends(get_current_active_user)])
def get_cleaning_tasks(status: str = None, db: Session = Depends(get_db)):
    return CleaningService.get_tasks(db, status=status)

@router.post("/{task_id}/complete", response_model=CleaningTaskResponse, dependencies=[Depends(get_current_active_user)])
def complete_cleaning_task(task_id: int, db: Session = Depends(get_db)):
    return CleaningService.complete_task(db, task_id)