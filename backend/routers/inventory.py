from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

import sys
sys.path.append('..')

from database import get_db
from models import (
    InventoryCategory, InventoryItem, InventoryHistory, Alert
)
from schemas import (
    InventoryCategoryCreate, InventoryCategoryResponse,
    InventoryItemCreate, InventoryItemResponse, InventoryItemUpdate,
    InventoryHistoryResponse, AlertCreate, AlertResponse
)

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


# Categories
@router.get("/categories", response_model=List[InventoryCategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Ottieni tutte le categorie inventario"""
    categories = db.query(InventoryCategory).all()
    return categories


@router.post("/categories", response_model=InventoryCategoryResponse)
def create_category(category: InventoryCategoryCreate, db: Session = Depends(get_db)):
    """Crea nuova categoria"""
    db_category = InventoryCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# Items
@router.get("/items", response_model=List[InventoryItemResponse])
def get_inventory_items(
    apartment_id: Optional[int] = None,
    category_id: Optional[int] = None,
    low_stock: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Ottieni articoli inventario con filtri opzionali"""
    query = db.query(InventoryItem)
    
    if apartment_id:
        query = query.filter(InventoryItem.apartment_id == apartment_id)
    if category_id:
        query = query.filter(InventoryItem.category_id == category_id)
    if low_stock:
        query = query.filter(InventoryItem.quantity <= InventoryItem.min_quantity)
    
    items = query.all()
    return items


@router.get("/items/{item_id}", response_model=InventoryItemResponse)
def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """Ottieni articolo per ID"""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Articolo non trovato")
    return item


@router.post("/items", response_model=InventoryItemResponse)
def create_inventory_item(item: InventoryItemCreate, db: Session = Depends(get_db)):
    """Crea nuovo articolo in inventario"""
    db_item = InventoryItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/items/{item_id}", response_model=InventoryItemResponse)
def update_inventory_item(
    item_id: int,
    item_update: InventoryItemUpdate,
    db: Session = Depends(get_db)
):
    """Aggiorna quantità articolo inventario"""
    db_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Articolo non trovato")
    
    update_data = item_update.dict(exclude_unset=True)
    old_quantity = db_item.quantity
    
    # Aggiorna quantità
    if "quantity" in update_data:
        new_quantity = update_data["quantity"]
        
        # Crea record storico
        history = InventoryHistory(
            item_id=item_id,
            user_id=update_data.get("user_id"),
            old_quantity=old_quantity,
            new_quantity=new_quantity,
            change_reason=update_data.get("change_reason", "Aggiornamento manuale")
        )
        db.add(history)
        
        # Controlla se sotto scorta minima
        if new_quantity <= db_item.min_quantity:
            # Crea alert se non esiste già
            existing_alert = db.query(Alert).filter(
                Alert.inventory_item_id == item_id,
                Alert.resolved == False
            ).first()
            
            if not existing_alert:
                alert = Alert(
                    apartment_id=db_item.apartment_id,
                    inventory_item_id=item_id,
                    alert_type="low_stock",
                    message=f"Scorta bassa per {db_item.name}: {new_quantity} {db_item.unit}",
                    severity="high" if new_quantity == 0 else "medium"
                )
                db.add(alert)
    
    # Aggiorna item
    for key, value in update_data.items():
        if key not in ["user_id", "change_reason"]:
            setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/items/{item_id}")
def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """Elimina articolo da inventario"""
    db_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Articolo non trovato")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Articolo eliminato con successo"}


# History
@router.get("/items/{item_id}/history", response_model=List[InventoryHistoryResponse])
def get_item_history(item_id: int, db: Session = Depends(get_db)):
    """Ottieni storico modifiche per un articolo"""
    history = db.query(InventoryHistory).filter(
        InventoryHistory.item_id == item_id
    ).order_by(InventoryHistory.created_at.desc()).all()
    return history


# Alerts
@router.get("/alerts", response_model=List[AlertResponse])
def get_alerts(
    apartment_id: Optional[int] = None,
    resolved: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Ottieni alert con filtri"""
    query = db.query(Alert)
    
    if apartment_id:
        query = query.filter(Alert.apartment_id == apartment_id)
    if resolved is not None:
        query = query.filter(Alert.resolved == resolved)
    
    alerts = query.order_by(Alert.created_at.desc()).all()
    return alerts


@router.post("/alerts", response_model=AlertResponse)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """Crea nuovo alert"""
    db_alert = Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.put("/alerts/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    """Risolvi un alert"""
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert non trovato")
    
    db_alert.resolved = True
    db_alert.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(db_alert)
    return db_alert

