from sqlalchemy import String, DateTime, Integer,func
from sqlalchemy.orm import Mapped, Column, relationship
from typing import List
from project.database import Base

from models import MeetingAnalysis


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    email = Column(String(255))
    name = Column(String(255))
    hashed_password = Column(String(60))
    create_time = Column(DateTime, default=func.now())
    
    ### FK
    
    ### relationships
    analyses: Mapped[List["MeetingAnalysis"]] = relationship(backpopulates="user")