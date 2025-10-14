from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import sys
sys.path.append('..')

from database import get_db
from models import Apartment
from schemas import ApartmentCreate, ApartmentResponse

router = APIRouter(prefix="/api/apartments", tags=["apartments"])


@router.get("/", response_model=List[ApartmentResponse])
def get_apartments(db: Session = Depends(get_db)):
    """Ottieni lista di tutti gli appartamenti"""
    apartments = db.query(Apartment).all()
    return apartments


@router.post("/", response_model=ApartmentResponse)
def create_apartment(apartment: ApartmentCreate, db: Session = Depends(get_db)):
    """Crea nuovo appartamento"""
    db_apartment = Apartment(**apartment.dict())
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    return db_apartment


@router.get("/{apartment_id}", response_model=ApartmentResponse)
def get_apartment(apartment_id: int, db: Session = Depends(get_db)):
    """Ottieni appartamento per ID"""
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="Appartamento non trovato")
    return apartment


@router.put("/{apartment_id}", response_model=ApartmentResponse)
def update_apartment(apartment_id: int, apartment: ApartmentCreate, db: Session = Depends(get_db)):
    """Aggiorna appartamento"""
    db_apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not db_apartment:
        raise HTTPException(status_code=404, detail="Appartamento non trovato")
    
    for key, value in apartment.dict().items():
        setattr(db_apartment, key, value)
    
    db.commit()
    db.refresh(db_apartment)
    return db_apartment


@router.delete("/{apartment_id}")
def delete_apartment(apartment_id: int, db: Session = Depends(get_db)):
    """Elimina appartamento"""
    db_apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not db_apartment:
        raise HTTPException(status_code=404, detail="Appartamento non trovato")
    
    db.delete(db_apartment)
    db.commit()
    return {"message": "Appartamento eliminato con successo"}



