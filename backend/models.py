from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class UserRole(str, enum.Enum):
    OPERATORE = "operatore"
    MANAGER = "manager"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)  # Nome completo per visualizzazione
    role = Column(Enum(UserRole), default=UserRole.OPERATORE)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazioni
    checklists = relationship("Checklist", back_populates="user")


class Apartment(Base):
    __tablename__ = "apartments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # es: "Appartamento 1", "Appartamento 2"
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazioni
    checklists = relationship("Checklist", back_populates="apartment")
    inventory_items = relationship("InventoryItem", back_populates="apartment")


class ChecklistTemplate(Base):
    __tablename__ = "checklist_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    apartment_id = Column(Integer, ForeignKey("apartments.id"), nullable=True)  # null = template generale
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazioni
    apartment = relationship("Apartment")
    tasks = relationship("TaskTemplate", back_populates="template")


class TaskTemplate(Base):
    __tablename__ = "task_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("checklist_templates.id"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    task_type = Column(String, default="checkbox")  # checkbox, text, yes_no, photo
    order_index = Column(Integer, default=0)
    required = Column(Boolean, default=False)
    
    # Relazioni
    template = relationship("ChecklistTemplate", back_populates="tasks")


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
    task_responses = relationship("TaskResponse", back_populates="checklist", cascade="all, delete-orphan")


class TaskResponse(Base):
    __tablename__ = "task_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    checklist_id = Column(Integer, ForeignKey("checklists.id"))
    task_template_id = Column(Integer, ForeignKey("task_templates.id"))
    completed = Column(Boolean, default=False)
    text_response = Column(Text, nullable=True)
    yes_no_response = Column(Boolean, nullable=True)
    photo_paths = Column(Text, nullable=True)  # JSON array di percorsi
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relazioni
    checklist = relationship("Checklist", back_populates="task_responses")
    task_template = relationship("TaskTemplate")


class InventoryCategory(Base):
    __tablename__ = "inventory_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    is_consumable = Column(Boolean, default=False)  # True per materiali di consumo
    
    # Relazioni
    items = relationship("InventoryItem", back_populates="category")


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    apartment_id = Column(Integer, ForeignKey("apartments.id"))
    category_id = Column(Integer, ForeignKey("inventory_categories.id"))
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    min_quantity = Column(Integer, default=0)  # Soglia minima per alert
    unit = Column(String, default="pz")  # pz, kg, litri, ecc.
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relazioni
    apartment = relationship("Apartment", back_populates="inventory_items")
    category = relationship("InventoryCategory", back_populates="items")
    user = relationship("User")
    history = relationship("InventoryHistory", back_populates="item")


class InventoryHistory(Base):
    __tablename__ = "inventory_history"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("inventory_items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    old_quantity = Column(Integer)
    new_quantity = Column(Integer)
    change_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazioni
    item = relationship("InventoryItem", back_populates="history")
    user = relationship("User")


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    apartment_id = Column(Integer, ForeignKey("apartments.id"))
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=True)
    alert_type = Column(String)  # low_stock, missing_item, checklist_issue
    message = Column(Text)
    severity = Column(String, default="medium")  # low, medium, high
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relazioni
    apartment = relationship("Apartment")
    inventory_item = relationship("InventoryItem")



