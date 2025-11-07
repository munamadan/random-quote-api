from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

Base = declarative_base()

# SQLAlchemy Models
class QuoteDB(Base):
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    category = Column(String(50), default="general")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Pydantic Models
class QuoteBase(BaseModel):
    text: str
    author: str
    category: Optional[str] = "general"

class QuoteCreate(QuoteBase):
    pass

class QuoteUpdate(BaseModel):
    text: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None

class Quote(QuoteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  

class QuoteResponse(BaseModel):
    success: bool
    data: Optional[Quote] = None
    message: Optional[str] = None
    
    class Config:
        from_attributes = True  