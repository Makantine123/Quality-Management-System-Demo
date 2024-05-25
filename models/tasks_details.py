"""Task Details Module"""

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class TaskDetails(BaseModel):
    """Task Details Class"""
    __tablename__ = 'tasks_details'

    task_id = Column(String(60), ForeignKey('tasks.id'), nullable=False)
    investigation_id = Column(String(60),
                              ForeignKey('investigations.id'),
                              nullable=False)
    feedback = Column(String(255), nullable=False)
    attachment_name = Column(String(60), nullable=False)
    attachment_comments = Column(String(255), nullable=False)
    date_updated_on = Column(DateTime, nullable=False, onupdate=func.now())
    date_completed_on = Column(DateTime, nullable=False, default=func.now())

    tasks = relationship('Tasks', backref='tasks')
    investigations = relationship('Investigations', backref='investigations_task_details')
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
