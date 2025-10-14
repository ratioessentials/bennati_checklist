from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from models import UserRole


# User Schemas
class UserBase(BaseModel):
    name: str
    role: UserRole = UserRole.OPERATORE


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Apartment Schemas
class ApartmentBase(BaseModel):
    name: str
    description: Optional[str] = None


class ApartmentCreate(ApartmentBase):
    pass


class ApartmentResponse(ApartmentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Task Template Schemas
class TaskTemplateBase(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: str = "checkbox"
    order_index: int = 0
    required: bool = False


class TaskTemplateCreate(TaskTemplateBase):
    template_id: int


class TaskTemplateResponse(TaskTemplateBase):
    id: int
    template_id: int
    
    class Config:
        from_attributes = True


# Checklist Template Schemas
class ChecklistTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    apartment_id: Optional[int] = None


class ChecklistTemplateCreate(ChecklistTemplateBase):
    tasks: List[TaskTemplateBase] = []


class ChecklistTemplateResponse(ChecklistTemplateBase):
    id: int
    created_at: datetime
    tasks: List[TaskTemplateResponse] = []
    
    class Config:
        from_attributes = True


# Task Response Schemas
class TaskResponseBase(BaseModel):
    task_template_id: int
    completed: bool = False
    text_response: Optional[str] = None
    yes_no_response: Optional[bool] = None
    photo_paths: Optional[str] = None


class TaskResponseCreate(TaskResponseBase):
    checklist_id: int


class TaskResponseUpdate(BaseModel):
    completed: Optional[bool] = None
    text_response: Optional[str] = None
    yes_no_response: Optional[bool] = None
    photo_paths: Optional[str] = None


class TaskResponseResponse(TaskResponseBase):
    id: int
    checklist_id: int
    created_at: datetime
    updated_at: datetime
    task_template: Optional[TaskTemplateResponse] = None
    
    class Config:
        from_attributes = True


# Checklist Schemas
class ChecklistBase(BaseModel):
    apartment_id: int
    notes: Optional[str] = None


class ChecklistCreate(ChecklistBase):
    user_id: int


class ChecklistUpdate(BaseModel):
    completed: Optional[bool] = None
    notes: Optional[str] = None


class ChecklistResponse(ChecklistBase):
    id: int
    user_id: int
    date: datetime
    completed: bool
    completed_at: Optional[datetime] = None
    task_responses: List[TaskResponseResponse] = []
    
    class Config:
        from_attributes = True


# Inventory Schemas
class InventoryCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_consumable: bool = False


class InventoryCategoryCreate(InventoryCategoryBase):
    pass


class InventoryCategoryResponse(InventoryCategoryBase):
    id: int
    
    class Config:
        from_attributes = True


class InventoryItemBase(BaseModel):
    name: str
    quantity: int = 0
    min_quantity: int = 0
    unit: str = "pz"


class InventoryItemCreate(InventoryItemBase):
    apartment_id: int
    category_id: int


class InventoryItemUpdate(BaseModel):
    quantity: Optional[int] = None
    min_quantity: Optional[int] = None
    user_id: Optional[int] = None
    change_reason: Optional[str] = None


class InventoryItemResponse(InventoryItemBase):
    id: int
    apartment_id: int
    category_id: int
    last_updated: datetime
    last_updated_by: Optional[int] = None
    category: Optional[InventoryCategoryResponse] = None
    
    class Config:
        from_attributes = True


class InventoryHistoryResponse(BaseModel):
    id: int
    item_id: int
    user_id: int
    old_quantity: int
    new_quantity: int
    change_reason: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Alert Schemas
class AlertBase(BaseModel):
    apartment_id: int
    alert_type: str
    message: str
    severity: str = "medium"


class AlertCreate(AlertBase):
    inventory_item_id: Optional[int] = None


class AlertResponse(AlertBase):
    id: int
    inventory_item_id: Optional[int] = None
    resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Login Schema
class LoginRequest(BaseModel):
    name: str
    apartment_id: int
    date: Optional[datetime] = None


class LoginResponse(BaseModel):
    user: UserResponse
    apartment: ApartmentResponse
    checklist: ChecklistResponse


# Dashboard/Report Schemas
class ApartmentInventoryReport(BaseModel):
    apartment: ApartmentResponse
    low_stock_items: List[InventoryItemResponse]
    missing_items: List[InventoryItemResponse]
    total_items: int


class ManagerDashboard(BaseModel):
    apartments: List[ApartmentInventoryReport]
    active_alerts: List[AlertResponse]
    recent_checklists: List[ChecklistResponse]
    items_to_restock: List[InventoryItemResponse]



