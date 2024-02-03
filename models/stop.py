#!/usr/bin/python3
"""This module defines a Schedule class."""
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship


class BusStop(BaseModel, Base):
    """Class to represent a bus stop."""

    __tablename__ = 'bus_stops'

    route_id: Mapped[str] = mapped_column(ForeignKey('routes.id'), nullable=False)
    route: Mapped['Route'] = relationship(back_populates='stops')

    stop_number_in_route: Mapped[int] = mapped_column(nullable=False)
    stop_name: Mapped[str] = mapped_column(String(60), nullable=False)
    place: Mapped[str] = mapped_column(String(128), nullable=True)
    is_terminus: Mapped[bool] = mapped_column(nullable=True, default=False)
    