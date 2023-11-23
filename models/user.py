#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from models.feedback import Feedback
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship
from typing import List
#import hashlib


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    feedback: Mapped[List['Feedback']] = relationship(back_populates='user')
    #def __init__(self, *args, **kwargs):
    #    """initializes user"""
    #    super().__init__(*args, **kwargs)

    #@property
    #def password(self):
    #    return self._password

    #@password.setter
    #def password(self, pwd):
    #    """hashing password values"""
    #   self._password = hashlib.md5(pwd.encode()).hexdigest()