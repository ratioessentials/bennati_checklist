from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfgen import canvas
import csv
import io

import sys
sys.path.append('..')

from database import get_db
from models import (
    Apartment, InventoryItem, Alert, Checklist, User
)
from schemas import (
    ManagerDashboard, ApartmentInventoryReport,
    InventoryItemResponse, AlertResponse, ChecklistResponse
)

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/dashboard", response_model=ManagerDashboard)
def get_manager_dashboard(db: Session = Depends(get_db)):
    """
    Dashboard completa per manager con:
    - Inventario per appartamento
    - Alert attivi
    - Checklist recenti
    - Articoli da riordinare
    """
    apartments = db.query(Apartment).all()
    apartment_reports = []
    
    for apt in apartments:
        # Articoli sotto scorta minima
        low_stock = db.query(InventoryItem).filter(
            InventoryItem.apartment_id == apt.id,
            InventoryItem.quantity <= InventoryItem.min_quantity,
            InventoryItem.quantity > 0
        ).all()
        
        # Articoli mancanti (quantità = 0)
        missing = db.query(InventoryItem).filter(
            InventoryItem.apartment_id == apt.id,
            InventoryItem.quantity == 0
        ).all()
        
        total_items = db.query(InventoryItem).filter(
            InventoryItem.apartment_id == apt.id
        ).count()
        
        apartment_reports.append({
            "apartment": apt,
            "low_stock_items": low_stock,
            "missing_items": missing,
            "total_items": total_items
        })
    
    # Alert attivi
    active_alerts = db.query(Alert).filter(
        Alert.resolved == False
    ).order_by(Alert.created_at.desc()).limit(20).all()
    
    # Checklist recenti (ultimi 7 giorni)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_checklists = db.query(Checklist).filter(
        Checklist.date >= seven_days_ago
    ).order_by(Checklist.date.desc()).limit(20).all()
    
    # Tutti gli articoli da riordinare (sotto scorta)
    items_to_restock = db.query(InventoryItem).filter(
        InventoryItem.quantity <= InventoryItem.min_quantity
    ).order_by(InventoryItem.quantity.asc()).all()
    
    return {
        "apartments": apartment_reports,
        "active_alerts": active_alerts,
        "recent_checklists": recent_checklists,
        "items_to_restock": items_to_restock
    }


@router.get("/apartment/{apartment_id}/inventory")
def get_apartment_inventory_report(apartment_id: int, db: Session = Depends(get_db)):
    """Report inventario dettagliato per appartamento"""
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="Appartamento non trovato")
    
    items = db.query(InventoryItem).filter(
        InventoryItem.apartment_id == apartment_id
    ).all()
    
    low_stock = [item for item in items if item.quantity <= item.min_quantity and item.quantity > 0]
    missing = [item for item in items if item.quantity == 0]
    ok_stock = [item for item in items if item.quantity > item.min_quantity]
    
    return {
        "apartment": apartment,
        "total_items": len(items),
        "low_stock_count": len(low_stock),
        "missing_count": len(missing),
        "ok_stock_count": len(ok_stock),
        "low_stock_items": low_stock,
        "missing_items": missing,
        "all_items": items
    }


@router.get("/export/inventory/pdf")
def export_inventory_pdf(apartment_id: int = None, db: Session = Depends(get_db)):
    """Esporta inventario in PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Titolo
    title = Paragraph("Report Inventario", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Query items
    query = db.query(InventoryItem)
    if apartment_id:
        query = query.filter(InventoryItem.apartment_id == apartment_id)
        apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
        if apartment:
            subtitle = Paragraph(f"Appartamento: {apartment.name}", styles['Heading2'])
            elements.append(subtitle)
            elements.append(Spacer(1, 12))
    
    items = query.all()
    
    # Crea tabella
    data = [['Articolo', 'Quantità', 'Min.', 'Unità', 'Stato']]
    for item in items:
        status = "OK" if item.quantity > item.min_quantity else ("BASSO" if item.quantity > 0 else "MANCANTE")
        data.append([
            item.name,
            str(item.quantity),
            str(item.min_quantity),
            item.unit,
            status
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=inventory_report_{datetime.utcnow().strftime('%Y%m%d')}.pdf"}
    )


@router.get("/export/inventory/csv")
def export_inventory_csv(apartment_id: int = None, db: Session = Depends(get_db)):
    """Esporta inventario in CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['ID', 'Appartamento', 'Articolo', 'Categoria', 'Quantità', 'Minimo', 'Unità', 'Stato', 'Ultimo Aggiornamento'])
    
    # Query
    query = db.query(InventoryItem)
    if apartment_id:
        query = query.filter(InventoryItem.apartment_id == apartment_id)
    
    items = query.all()
    
    for item in items:
        status = "OK" if item.quantity > item.min_quantity else ("BASSO" if item.quantity > 0 else "MANCANTE")
        writer.writerow([
            item.id,
            item.apartment.name if item.apartment else '',
            item.name,
            item.category.name if item.category else '',
            item.quantity,
            item.min_quantity,
            item.unit,
            status,
            item.last_updated.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=inventory_export_{datetime.utcnow().strftime('%Y%m%d')}.csv"}
    )


@router.get("/export/checklists/csv")
def export_checklists_csv(
    apartment_id: int = None,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    """Esporta checklist in CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['ID', 'Data', 'Appartamento', 'Operatore', 'Completata', 'Note'])
    
    # Query
    query = db.query(Checklist)
    if apartment_id:
        query = query.filter(Checklist.apartment_id == apartment_id)
    if start_date:
        query = query.filter(Checklist.date >= start_date)
    if end_date:
        query = query.filter(Checklist.date <= end_date)
    
    checklists = query.order_by(Checklist.date.desc()).all()
    
    for checklist in checklists:
        writer.writerow([
            checklist.id,
            checklist.date.strftime('%Y-%m-%d %H:%M:%S'),
            checklist.apartment.name if checklist.apartment else '',
            checklist.user.name if checklist.user else '',
            'Sì' if checklist.completed else 'No',
            checklist.notes or ''
        ])
    
    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=checklists_export_{datetime.utcnow().strftime('%Y%m%d')}.csv"}
    )


@router.get("/stats/apartment/{apartment_id}")
def get_apartment_statistics(apartment_id: int, db: Session = Depends(get_db)):
    """Statistiche per appartamento"""
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="Appartamento non trovato")
    
    # Conta checklist
    total_checklists = db.query(Checklist).filter(
        Checklist.apartment_id == apartment_id
    ).count()
    
    completed_checklists = db.query(Checklist).filter(
        Checklist.apartment_id == apartment_id,
        Checklist.completed == True
    ).count()
    
    # Checklist ultimi 30 giorni
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_checklists = db.query(Checklist).filter(
        Checklist.apartment_id == apartment_id,
        Checklist.date >= thirty_days_ago
    ).count()
    
    # Inventario
    total_items = db.query(InventoryItem).filter(
        InventoryItem.apartment_id == apartment_id
    ).count()
    
    low_stock_items = db.query(InventoryItem).filter(
        InventoryItem.apartment_id == apartment_id,
        InventoryItem.quantity <= InventoryItem.min_quantity
    ).count()
    
    return {
        "apartment": apartment,
        "total_checklists": total_checklists,
        "completed_checklists": completed_checklists,
        "completion_rate": (completed_checklists / total_checklists * 100) if total_checklists > 0 else 0,
        "recent_checklists_30d": recent_checklists,
        "total_inventory_items": total_items,
        "low_stock_items": low_stock_items
    }



