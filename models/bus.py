#!/usr/bin/python3
"""This module defines a class Bus"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship


class Bus(BaseModel, Base):
    """This class defines a Bus by various attributes"""
    __tablename__ = 'buses'

    route_id: Mapped[str] = mapped_column(ForeignKey('routes.id'), nullable=False)
    route: Mapped['Route'] = relationship(back_populates='buses')
    
    bus_number: Mapped[int] = mapped_column(nullable=False) # bus number in a route
    capacity: Mapped[int] = mapped_column(nullable=True)
    current_location: Mapped[str] = mapped_column(String(128), nullable=True)

