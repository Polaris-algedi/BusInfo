#!/usr/bin/python3
"""This module defines a Schedule class."""
from datetime import time, timedelta
from models.base_model import BaseModel, Base
from models.route import Route
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship
from typing import List


class Schedule(BaseModel, Base):
    """Class to represent a schedule."""

    __tablename__ = 'schedules'

    first_departure: Mapped[time] = mapped_column(nullable=False, default=time(hour=6))
    last_departure: Mapped[time] = mapped_column(nullable=False, default=time(hour=21))
    duration: Mapped[timedelta] = mapped_column(nullable=False, default=timedelta(hours=1))
    bus_frequency: Mapped[timedelta] = mapped_column(nullable=False, default=timedelta(minutes=20))
    day_of_week: Mapped[str] = mapped_column(String(60), nullable=True)
    routes: Mapped[List['Route']] = relationship(back_populates='schedule', cascade="all, delete-orphan")