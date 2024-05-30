from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Revisions(BaseModel):
    """Revisions Class"""
    __tablename__ = "revisions"

    investigation_id = Column(String(60), ForeignKey('investigations.id'))
    requested_by = Column(String(60), nullable=False)
    reason_for_revision = Column(String(255), nullable=False)
    revison_type = Column(String(20), nullable=False)
    approved_by = Column(String(60), nullable=False)

    investigations = relationship('Investigations', backref='investigations')

    def __init__(self, *args, **kwargs) -> None:
        """Initialisation of class"""
        super().__init__(*args, **kwargs)
