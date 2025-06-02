from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

import datetime



class Vendor(Base):
    __tablename__ = "Vendor"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    textId = Column(String(255))
    title = Column(String(255), nullable=True)
    details = Column(Text, nullable=True)
    memberEmail = Column(String(150), nullable=True)
    url = Column(String, nullable=True)
    status = Column(String(1), default='Y')
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), nullable=True, default=None)

