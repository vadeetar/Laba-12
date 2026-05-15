from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class CleaningTask(Base):
    __tablename__ = "cleaning_tasks"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    assigned_to = Column(String, nullable=True)
    status = Column(String, default="pending") # pending, in_progress, done
    notes = Column(String, nullable=True)

    room = relationship("Room", back_populates="cleaning_tasks")