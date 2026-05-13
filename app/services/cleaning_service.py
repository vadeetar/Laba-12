from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.cleaning_task import CleaningTask
from app.models.room import Room


class CleaningService:
    @staticmethod
    def get_tasks(db: Session, status: str = None):
        query = db.query(CleaningTask)
        if status:
            query = query.filter(CleaningTask.status == status)
        return query.all()

    @staticmethod
    def complete_task(db: Session, task_id: int):
        task = db.query(CleaningTask).filter(CleaningTask.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        task.status = "done"

        # Уборка завершена -> комната снова доступна
        room = db.query(Room).filter(Room.id == task.room_id).first()
        if room:
            room.status = "available"

        db.commit()
        db.refresh(task)
        return task