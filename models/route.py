#!/usr/bin/python3
"""This module defines a class route"""
from models.base_model import BaseModel, Base
from models.feedback import Feedback
from models.bus import Bus
from models.stop import BusStop
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List


class Route(BaseModel, Base):
    """This class defines a route by various attributes"""
    __tablename__ = 'routes'

    schedule_id: Mapped[str] = mapped_column(ForeignKey('schedules.id'), nullable=False)
    schedule: Mapped['Schedule'] = relationship(back_populates='routes')

    
    line_number: Mapped[int] = mapped_column(nullable=False)
    urban: Mapped[bool] = mapped_column(nullable=False)

    departure_terminus: Mapped[str] = mapped_column(String(128), nullable=False)
    arrival_terminus: Mapped[str] = mapped_column(String(128), nullable=False)

    feedbacks: Mapped[List['Feedback']] = relationship(back_populates='route')
    buses: Mapped[List['Bus']] = relationship(back_populates='route')
    stops: Mapped[List['BusStop']] = relationship(back_populates='route')