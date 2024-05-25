""" Users Modules """

from werkzeug.security import check_password_hash, generate_password_hash
from models.base_model import BaseModel
from sqlalchemy import Column, String
from flask_login import UserMixin


class Users(BaseModel, UserMixin):
    """Users class"""
    __tablename__ = 'users'

    name = Column(String(60), nullable=True)
    surname = Column(String(60), nullable=True)
    email = Column(String(60), nullable=False, unique=True)
    _password_hsh = Column('password_hsh', String(100), nullable=False)
    github_signup = Column(String(20), nullable=True, default='Null')
    google_signup = Column(String(20), nullable=True, default='Null')
    standard_signup = Column(String(20), nullable=True, default='Null')

    def __init__(self, *args, **kwargs) -> None:
        """ Initialisation of class """
        super().__init__(*args, **kwargs)

    @property
    def password_hsh(self):
        """The password_hsh property."""
        return self._password_hsh

    @password_hsh.setter
    def password_hsh(self, password):
        """ Encript Password """
        hash = 'pbkdf2:sha1'
        self._password_hsh = generate_password_hash(password, method=hash)

    def check_password(self, password_hash, password):
        """ Check Password matches Encription return True or False"""
        return check_password_hash(password_hash, password)
