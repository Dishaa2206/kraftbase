from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    forms = relationship("Form", back_populates="creator")

class Form(Base):
    __tablename__ = "forms"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    fields = Column(JSON, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    submissions = relationship("FormSubmission", back_populates="form")
    creator = relationship("User", back_populates="forms")


class FormSubmission(Base):
    __tablename__ = "form_submissions"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    form_id = Column(Integer, ForeignKey("forms.id"), nullable=False)
    data = Column(JSON, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    form = relationship("Form", back_populates="submissions")
