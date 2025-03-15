from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    language_level = Column(String, default="Intermediate")
    is_premium = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_1 = Column(Integer, ForeignKey("users.id"))
    user_2 = Column(Integer, ForeignKey("users.id"))
    topic = Column(String)
    started_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    ended_at = Column(TIMESTAMP, nullable=True)
