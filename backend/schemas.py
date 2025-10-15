from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# User schemas
class UserBase(BaseModel):
    username: str
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Apartment schemas
class ApartmentBase(BaseModel):
    name: str
    description: Optional[str] = None

class Apartment(ApartmentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Task schemas
class TaskBase(BaseModel):
    description: str
    order_index: int = 0

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    checklist_id: int
    completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Checklist schemas
class ChecklistBase(BaseModel):
    apartment_id: int
    notes: Optional[str] = None

class ChecklistCreate(ChecklistBase):
    pass

class Checklist(ChecklistBase):
    id: int
    user_id: int
    date: datetime
    completed: bool
    completed_at: Optional[datetime] = None
    tasks: List[Task] = []
    
    class Config:
        from_attributes = True

# Login schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[User] = None
    token: Optional[str] = None
