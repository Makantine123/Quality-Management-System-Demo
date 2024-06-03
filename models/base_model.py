"""Base Model Class"""

from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.sql import functions, func


class StatusList:
    """Status Class Options"""
    OPT1 = "Registed"
    OPT2 = "In Progress"
    OPT3 = "Completed"
    OPT4 = "Approved"
    OPT5 = "Rejected"
    OPT6 = "Overdue"


@as_declarative()
class BaseModel:
    """Base Model Class For all Tables"""
    __abstract__ = True
    id = Column(String(60), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    date_created_on = Column(DateTime, nullable=False, default=func.now())
    date_updated_on = Column(DateTime, nullable=False, default=func.now(),
                             onupdate=functions.now())
    status = Column(String(60), nullable=False, default=StatusList.OPT2)

    def __init__(self, *args, **kwargs):
        """Initialisation of class"""

    @staticmethod
    def as_dict(self) -> dict:
        """Returns dictionary represetation of class / table"""
        mydict = {}
        for column in self.__table__.columns:
            column_name = column.name
            value = getattr(self, column_name)
            mydict[column_name] = value
        mydict["class"] = self.__class__.__name__
        if "_sa_instance_state" in mydict:
            del mydict["_sa_instance_state"]
        return mydict

    @staticmethod
    def to_datetime_string(dt):
        """ Convert a datetime object to a string """
        return dt.strftime('%Y-%m-%dT%H:%M')

    @staticmethod
    def from_datetime_string(dt_str):
        """ Convert a string to a datetime object """
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M')
