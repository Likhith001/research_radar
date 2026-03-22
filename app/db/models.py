from sqlalchemy import Column, Integer, String, Text
from .database import Base
from sqlalchemy import Column, Integer, String, Text, Float

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    abstract = Column(Text)
    summary = Column(Text)
    link = Column(String, unique=True)
    score = Column(Float)