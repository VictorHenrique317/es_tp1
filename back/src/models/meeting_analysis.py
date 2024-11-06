from sqlalchemy import String, DateTime, Integer, func, Column
from src.database import Base

class MeetingAnalysis(Base):
    __tablename__ = "meeting_analysis"
    
    id =  Column(Integer, primary_key=True)
    creation_time = Column(DateTime, default=func.now())
    
    media_path = Column(String(1024))
    transcription_path = Column(String(1024)) # Definir tamanho maximo
    summary_path = Column(String(1024))