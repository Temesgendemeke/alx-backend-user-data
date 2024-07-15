#!/usr/bin/env python3
"""user documentation"""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///user.db", echo=False)
Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=False)
    reset_token = Column(String(250), nullable=False)


Base.metadata.create_all(engine)

