#!/usr/bin/python3
"""This module defines a class feedback"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Feedback(BaseModel, Base):
    """Class to represent a feedback."""
    __tablename__ = 'feedbacks'

    # Columns representing foreign keys and relationships
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'), nullable=False)
    route_id: Mapped[str] = mapped_column(ForeignKey('routes.id'), nullable=False)

    # Relationships with other tables
    route: Mapped['Route'] = relationship(back_populates='feedbacks')
    user: Mapped['User'] = relationship(back_populates='feedbacks')

    # Feedback-specific attributes
    rating: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(String(1000), nullable=True) 
    