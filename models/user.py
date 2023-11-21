#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
#from sqlalchemy.orm import relationship
#import hashlib


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

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