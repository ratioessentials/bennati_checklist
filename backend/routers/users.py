from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

import sys
sys.path.append('..')

from database import get_db
from models import User, Apartment, Checklist, ChecklistTemplate, TaskTemplate, TaskResponse
from schemas import (
    UserCreate, UserResponse, LoginRequest, LoginResponse,
    ChecklistResponse, ApartmentResponse
)
from auth import create_access_token

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login dell'operatore: crea/recupera utente, crea nuova checklist per l'appartamento
    """
    # Trova o crea utente
    user = db.query(User).filter(User.name == login_data.name).first()
    if not user:
        user = User(name=login_data.name, role="operatore")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Verifica che l'appartamento esista
    apartment = db.query(Apartment).filter(Apartment.id == login_data.apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="Appartamento non trovato")
    
    # Crea nuova checklist per questa sessione
    checklist = Checklist(
        user_id=user.id,
        apartment_id=apartment.id,
        date=login_data.date or datetime.utcnow(),
        completed=False
    )
    db.add(checklist)
    db.commit()
    db.refresh(checklist)
    
    # Trova il template della checklist per questo appartamento
    template = db.query(ChecklistTemplate).filter(
        ChecklistTemplate.apartment_id == apartment.id
    ).first()
    
    # Se non esiste template specifico, usa quello generale
    if not template:
        template = db.query(ChecklistTemplate).filter(
            ChecklistTemplate.apartment_id.is_(None)
        ).first()
    
    # Crea task responses vuote per ogni task nel template
    if template:
        tasks = db.query(TaskTemplate).filter(
            TaskTemplate.template_id == template.id
        ).order_by(TaskTemplate.order_index).all()
        
        for task in tasks:
            task_response = TaskResponse(
                checklist_id=checklist.id,
                task_template_id=task.id,
                completed=False
            )
            db.add(task_response)
        
        db.commit()
    
    # Ricarica checklist con le task responses
    db.refresh(checklist)
    
    # Crea token di accesso
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    
    return {
        "user": user,
        "apartment": apartment,
        "checklist": checklist,
        "access_token": access_token
    }


@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Ottieni lista di tutti gli utenti"""
    users = db.query(User).all()
    return users


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crea nuovo utente"""
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Ottieni utente per ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return user



