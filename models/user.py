#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from models.feedback import Feedback
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
import hashlib
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


class User(BaseModel, Base):
    """Class to represent a user."""
    __tablename__ = 'users'

    # Define columns using the declarative syntax
    _email: Mapped[str] = mapped_column(String(128), nullable=False)
    _password: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)

    # Establish relationship with Feedback class
    feedbacks: Mapped[List['Feedback']] = relationship(back_populates='user', cascade='all, delete-orphan')

    
    def __init__(self, *args, **kwargs):
        # Pass values to property setters
        self.email = kwargs['email']
        self.password = kwargs['password']
        # Delete email and password to avoid duplicates
        del kwargs['email']
        del kwargs['password']
        
        super().__init__(*args, **kwargs)
        
        

    # Property and setter for email
    @property
    def email(self):
        """Getter method for the email."""
        return self._email

    @email.setter
    def email(self, value):
        """Setter method for setting the email."""
        if not EMAIL_REGEX.match(value):
            raise ValueError("Invalid email address")
        self._email = value

    # Property and setter for password
    @property
    def password(self):
        """Getter for password"""
        return self._password

    @password.setter
    def password(self, pwd):
        """Setter for hashing password values"""
        self._password = hashlib.md5(pwd.encode()).hexdigest()