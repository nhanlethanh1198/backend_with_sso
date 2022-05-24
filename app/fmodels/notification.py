from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Text, JSON, ARRAY
from sqlalchemy.orm import relationship

from app.database import Base


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    content = Column(Text)
    image = Column(String)
    type = Column(String)
    detail = Column(JSON, nullable=True, default=None)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
