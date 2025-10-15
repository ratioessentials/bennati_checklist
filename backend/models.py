from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazioni
    checklists = relationship("Checklist", back_populates="user")

class Apartment(Base):
    __tablename__ = "apartments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazioni
    checklists = relationship("Checklist", back_populates="apartment")

class Checklist(Base):
    __tablename__ = "checklists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    apartment_id = Column(Integer, ForeignKey("apartments.id"))
    date = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relazioni
    user = relationship("User", back_populates="checklists")
    apartment = relationship("Apartment", back_populates="checklists")
    tasks = relationship("Task", back_populates="checklist", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    checklist_id = Column(Integer, ForeignKey("checklists.id"))
    description = Column(String)
    completed = Column(Boolean, default=False)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazioni
    checklist = relationship("Checklist", back_populates="tasks")
