#!/usr/bin/python3
"""This module defines a class feedback"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship


class Feedback(BaseModel, Base):
    """This class defines a feedback by various attributes"""
    __tablename__ = 'feedbacks'

    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'), nullable=False)
    route_id: Mapped[str] = mapped_column(ForeignKey('routes.id'), nullable=False)
    route: Mapped['Route'] = relationship(back_populates='feedback')
    user: Mapped['User'] = relationship(back_populates='feedback')
    rating: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(String(1000), nullable=True) 
    