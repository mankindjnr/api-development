from .database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import datetime

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    #updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    #updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)