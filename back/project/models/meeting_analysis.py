from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, Column, relationship
from project.database import Base

from models import User

class MeetingAnalysis(Base):
    __tablename__ = "meeting_analysis"
    
    id =  Column(primary_key=True)
    trascription = Column(String(1024)) # Definir tamanho maximo
    summary = Column(String(1024))
    
    ## FK
    user_id = Column(Integer, ForeignKey('user.id'))

    ## relationships
    # Many-to-one relationship with User
    user: Mapped["User"] = relationship(back_populates="analyses")