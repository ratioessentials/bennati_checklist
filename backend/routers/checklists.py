from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import json
import aiofiles
import uuid

import sys
sys.path.append('..')

from database import get_db
from models import Checklist, TaskResponse, ChecklistTemplate, TaskTemplate
from schemas import (
    ChecklistCreate, ChecklistResponse, ChecklistUpdate,
    TaskResponseCreate, TaskResponseResponse, TaskResponseUpdate,
    ChecklistTemplateCreate, ChecklistTemplateResponse,
    TaskTemplateCreate, TaskTemplateResponse
)

router = APIRouter(prefix="/api/checklists", tags=["checklists"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/", response_model=List[ChecklistResponse])
def get_checklists(
    apartment_id: Optional[int] = None,
    user_id: Optional[int] = None,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Ottieni lista checklist con filtri opzionali"""
    query = db.query(Checklist)
    
    if apartment_id:
        query = query.filter(Checklist.apartment_id == apartment_id)
    if user_id:
        query = query.filter(Checklist.user_id == user_id)
    if completed is not None:
        query = query.filter(Checklist.completed == completed)
    
    checklists = query.order_by(Checklist.date.desc()).all()
    return checklists


@router.get("/{checklist_id}", response_model=ChecklistResponse)
def get_checklist(checklist_id: int, db: Session = Depends(get_db)):
    """Ottieni checklist per ID con tutte le task responses"""
    checklist = db.query(Checklist).filter(Checklist.id == checklist_id).first()
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist non trovata")
    return checklist


@router.post("/", response_model=ChecklistResponse)
def create_checklist(checklist: ChecklistCreate, db: Session = Depends(get_db)):
    """Crea nuova checklist"""
    db_checklist = Checklist(**checklist.dict())
    db.add(db_checklist)
    db.commit()
    db.refresh(db_checklist)
    return db_checklist


@router.put("/{checklist_id}", response_model=ChecklistResponse)
def update_checklist(
    checklist_id: int,
    checklist_update: ChecklistUpdate,
    db: Session = Depends(get_db)
):
    """Aggiorna checklist (es: completamento)"""
    db_checklist = db.query(Checklist).filter(Checklist.id == checklist_id).first()
    if not db_checklist:
        raise HTTPException(status_code=404, detail="Checklist non trovata")
    
    update_data = checklist_update.dict(exclude_unset=True)
    
    # Se completata, imposta timestamp
    if update_data.get("completed") and not db_checklist.completed:
        update_data["completed_at"] = datetime.utcnow()
    
    for key, value in update_data.items():
        setattr(db_checklist, key, value)
    
    db.commit()
    db.refresh(db_checklist)
    return db_checklist


# Task Responses endpoints
@router.get("/{checklist_id}/tasks", response_model=List[TaskResponseResponse])
def get_checklist_tasks(checklist_id: int, db: Session = Depends(get_db)):
    """Ottieni tutte le task di una checklist"""
    tasks = db.query(TaskResponse).filter(
        TaskResponse.checklist_id == checklist_id
    ).all()
    return tasks


@router.put("/tasks/{task_response_id}", response_model=TaskResponseResponse)
def update_task_response(
    task_response_id: int,
    task_update: TaskResponseUpdate,
    db: Session = Depends(get_db)
):
    """Aggiorna risposta a una task"""
    db_task = db.query(TaskResponse).filter(TaskResponse.id == task_response_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task response non trovata")
    
    update_data = task_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    return db_task


@router.post("/tasks/{task_response_id}/upload")
async def upload_task_photo(
    task_response_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload foto/video per una task"""
    db_task = db.query(TaskResponse).filter(TaskResponse.id == task_response_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task response non trovata")
    
    # Genera nome file unico
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Salva file
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # Aggiorna photo_paths (JSON array)
    existing_paths = json.loads(db_task.photo_paths) if db_task.photo_paths else []
    existing_paths.append(unique_filename)
    db_task.photo_paths = json.dumps(existing_paths)
    db_task.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_task)
    
    return {
        "message": "File caricato con successo",
        "filename": unique_filename,
        "path": file_path
    }


# Checklist Templates endpoints
@router.get("/templates/", response_model=List[ChecklistTemplateResponse])
def get_templates(apartment_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Ottieni template checklist"""
    query = db.query(ChecklistTemplate)
    if apartment_id:
        query = query.filter(ChecklistTemplate.apartment_id == apartment_id)
    templates = query.all()
    return templates


@router.post("/templates/", response_model=ChecklistTemplateResponse)
def create_template(template: ChecklistTemplateCreate, db: Session = Depends(get_db)):
    """Crea nuovo template checklist"""
    # Crea template
    template_data = template.dict(exclude={"tasks"})
    db_template = ChecklistTemplate(**template_data)
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    
    # Crea tasks
    for idx, task in enumerate(template.tasks):
        task_data = task.dict()
        task_data["template_id"] = db_template.id
        task_data["order_index"] = idx
        db_task = TaskTemplate(**task_data)
        db.add(db_task)
    
    db.commit()
    db.refresh(db_template)
    return db_template


@router.get("/templates/{template_id}", response_model=ChecklistTemplateResponse)
def get_template(template_id: int, db: Session = Depends(get_db)):
    """Ottieni template per ID"""
    template = db.query(ChecklistTemplate).filter(ChecklistTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template non trovato")
    return template



