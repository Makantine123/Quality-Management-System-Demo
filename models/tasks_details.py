"""Task Details Module"""

import os
from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from werkzeug.utils import secure_filename
from models.base_model import BaseModel
from config import Config


class TaskDetails(BaseModel):
    """Task Details Class"""
    __tablename__ = 'tasks_details'

    task_id = Column(String(60), ForeignKey('tasks.id'), nullable=False)
    investigation_id = Column(String(60),
                              ForeignKey('investigations.id'),
                              nullable=False)
    feedback = Column(String(255), nullable=False)
    _attachment_name = Column("attachment_name", String(60), nullable=False)
    attachment_comments = Column(String(255), nullable=False)
    date_updated_on = Column(DateTime, nullable=False, onupdate=func.now())
    date_completed_on = Column(DateTime, nullable=True)

    tasks = relationship('Tasks', backref='tasks')
    investigations = relationship('Investigations',
                                  backref='investigations_task_details')

    def __init__(self, *args, **kwargs) -> None:
        """ Initialization of Class """
        super().__init__(*args, **kwargs)

    @staticmethod
    def allowed_file(filename):
        """ Veryfy if file extetion is allowed """
        allowed_extentions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'xlsx', 'docx'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extentions

    @property
    def attachment_name(self):
        """ The attachment_name property """
        return self._attachment_name

    @attachment_name.setter
    def attachment_name(self, file):
        """ Sets unique attachment name """
        if file and self.allowed_file(file):
            filename = secure_filename(file.filename)
            unique_filename = f'{uuid4().hex}_{filename}'
            file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            self._attachment_name = unique_filename
        else:
            raise ValueError("Invalid or file type not allowed")
