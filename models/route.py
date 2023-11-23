#!/usr/bin/python3
"""This module defines a class route"""
from models.base_model import BaseModel, Base
from models.feedback import Feedback
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List


class Route(BaseModel, Base):
    """This class defines a route by various attributes"""
    __tablename__ = 'routes'

    route_name: Mapped[str] = mapped_column(String(128), nullable=False)
    departure_terminus: Mapped[str] = mapped_column(String(128), nullable=False)
    arrival_terminus: Mapped[str] = mapped_column(String(128), nullable=False)
    frequency: Mapped[int] = mapped_column(nullable=False)
    feedback: Mapped[List['Feedback']] = relationship(back_populates='route')
