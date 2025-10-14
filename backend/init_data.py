"""
Script per inizializzare dati di esempio nel database
"""
from database import SessionLocal, engine, Base
from models import (
    Apartment, User, UserRole, InventoryCategory, InventoryItem,
    ChecklistTemplate, TaskTemplate
)

# Crea tabelle
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Crea appartamenti
    apartments = [
        Apartment(name="Appartamento 1", description="Piano terra, 2 camere"),
        Apartment(name="Appartamento 2", description="Primo piano, monolocale"),
        Apartment(name="Appartamento 3", description="Secondo piano, 3 camere"),
        Apartment(name="Appartamento 4", description="Attico, 2 camere con terrazzo")
    ]
    
    for apt in apartments:
        existing = db.query(Apartment).filter(Apartment.name == apt.name).first()
        if not existing:
            db.add(apt)
    
    db.commit()
    print("✅ Appartamenti creati")
    
    # Crea utente manager
    manager = db.query(User).filter(User.name == "Manager").first()
    if not manager:
        manager = User(name="Manager", role=UserRole.MANAGER)
        db.add(manager)
        db.commit()
    print("✅ Utente Manager creato")
    
    # Crea categorie inventario
    categories = [
        InventoryCategory(
            name="Cucina",
            description="Articoli per la cucina",
            is_consumable=False
        ),
        InventoryCategory(
            name="Bagno",
            description="Articoli per il bagno",
            is_consumable=False
        ),
        InventoryCategory(
            name="Camera",
            description="Articoli per la camera",
            is_consumable=False
        ),
        InventoryCategory(
            name="Consumabili",
            description="Materiali di consumo",
            is_consumable=True
        ),
        InventoryCategory(
            name="Pulizia",
            description="Prodotti per la pulizia",
            is_consumable=True
        )
    ]
    
    for cat in categories:
        existing = db.query(InventoryCategory).filter(InventoryCategory.name == cat.name).first()
        if not existing:
            db.add(cat)
    
    db.commit()
    print("✅ Categorie inventario create")
    
    # Recupera IDs
    apartments = db.query(Apartment).all()
    cucina_cat = db.query(InventoryCategory).filter(InventoryCategory.name == "Cucina").first()
    bagno_cat = db.query(InventoryCategory).filter(InventoryCategory.name == "Bagno").first()
    camera_cat = db.query(InventoryCategory).filter(InventoryCategory.name == "Camera").first()
    consumabili_cat = db.query(InventoryCategory).filter(InventoryCategory.name == "Consumabili").first()
    pulizia_cat = db.query(InventoryCategory).filter(InventoryCategory.name == "Pulizia").first()
    
    # Crea articoli inventario per ogni appartamento
    inventory_templates = [
        # Cucina
        {"name": "Bicchieri", "category_id": cucina_cat.id, "quantity": 6, "min_quantity": 4, "unit": "pz"},
        {"name": "Piatti", "category_id": cucina_cat.id, "quantity": 6, "min_quantity": 4, "unit": "pz"},
        {"name": "Posate", "category_id": cucina_cat.id, "quantity": 12, "min_quantity": 8, "unit": "pz"},
        {"name": "Pentole", "category_id": cucina_cat.id, "quantity": 3, "min_quantity": 2, "unit": "pz"},
        {"name": "Caffettiera/Macchina caffè", "category_id": cucina_cat.id, "quantity": 1, "min_quantity": 1, "unit": "pz"},
        
        # Bagno
        {"name": "Asciugamani grandi", "category_id": bagno_cat.id, "quantity": 4, "min_quantity": 2, "unit": "pz"},
        {"name": "Asciugamani piccoli", "category_id": bagno_cat.id, "quantity": 4, "min_quantity": 2, "unit": "pz"},
        {"name": "Tappetino bagno", "category_id": bagno_cat.id, "quantity": 1, "min_quantity": 1, "unit": "pz"},
        {"name": "Phon", "category_id": bagno_cat.id, "quantity": 1, "min_quantity": 1, "unit": "pz"},
        
        # Camera
        {"name": "Lenzuola", "category_id": camera_cat.id, "quantity": 2, "min_quantity": 1, "unit": "set"},
        {"name": "Coperte", "category_id": camera_cat.id, "quantity": 2, "min_quantity": 1, "unit": "pz"},
        {"name": "Cuscini", "category_id": camera_cat.id, "quantity": 4, "min_quantity": 2, "unit": "pz"},
        {"name": "Ferro da stiro", "category_id": camera_cat.id, "quantity": 1, "min_quantity": 1, "unit": "pz"},
        
        # Consumabili
        {"name": "Cialde caffè", "category_id": consumabili_cat.id, "quantity": 20, "min_quantity": 10, "unit": "pz"},
        {"name": "Carta igienica", "category_id": consumabili_cat.id, "quantity": 6, "min_quantity": 3, "unit": "rotoli"},
        {"name": "Sapone mani", "category_id": consumabili_cat.id, "quantity": 2, "min_quantity": 1, "unit": "pz"},
        {"name": "Shampoo/Bagnoschiuma", "category_id": consumabili_cat.id, "quantity": 2, "min_quantity": 1, "unit": "pz"},
        
        # Pulizia
        {"name": "Detersivo piatti", "category_id": pulizia_cat.id, "quantity": 1, "min_quantity": 1, "unit": "pz"},
        {"name": "Detersivo superfici", "category_id": pulizia_cat.id, "quantity": 1, "min_quantity": 1, "unit": "pz"},
        {"name": "Sacchetti spazzatura", "category_id": pulizia_cat.id, "quantity": 10, "min_quantity": 5, "unit": "pz"},
    ]
    
    for apt in apartments:
        for item_template in inventory_templates:
            existing = db.query(InventoryItem).filter(
                InventoryItem.apartment_id == apt.id,
                InventoryItem.name == item_template["name"]
            ).first()
            
            if not existing:
                item = InventoryItem(
                    apartment_id=apt.id,
                    **item_template
                )
                db.add(item)
    
    db.commit()
    print("✅ Articoli inventario creati per tutti gli appartamenti")
    
    # Crea template checklist generale
    existing_template = db.query(ChecklistTemplate).filter(
        ChecklistTemplate.name == "Checklist Standard Pulizia"
    ).first()
    
    if not existing_template:
        template = ChecklistTemplate(
            name="Checklist Standard Pulizia",
            description="Checklist standard per tutti gli appartamenti",
            apartment_id=None  # Template generale
        )
        db.add(template)
        db.commit()
        db.refresh(template)
        
        # Crea task del template
        tasks = [
            {"title": "Aspirare/lavare pavimenti", "task_type": "checkbox", "required": True, "order_index": 0},
            {"title": "Pulire bagno completo", "task_type": "checkbox", "required": True, "order_index": 1},
            {"title": "Cambiare biancheria letto", "task_type": "checkbox", "required": True, "order_index": 2},
            {"title": "Pulire cucina e fornelli", "task_type": "checkbox", "required": True, "order_index": 3},
            {"title": "Svuotare cestini", "task_type": "checkbox", "required": True, "order_index": 4},
            {"title": "Rifornire consumabili (carta, sapone, ecc.)", "task_type": "checkbox", "required": True, "order_index": 5},
            {"title": "Controllo inventario completato", "task_type": "yes_no", "required": True, "order_index": 6},
            {"title": "Foto dello stato finale", "task_type": "photo", "required": False, "order_index": 7},
            {"title": "Note aggiuntive o problemi riscontrati", "task_type": "text", "required": False, "order_index": 8},
        ]
        
        for task_data in tasks:
            task = TaskTemplate(template_id=template.id, **task_data)
            db.add(task)
        
        db.commit()
        print("✅ Template checklist creato con task")
    else:
        print("✅ Template checklist già esistente")
    
    print("\n🎉 Inizializzazione completata con successo!")
    print(f"   - {len(apartments)} appartamenti")
    print(f"   - {len(categories)} categorie inventario")
    print(f"   - {len(inventory_templates)} tipologie articoli per appartamento")
    print(f"   - 1 template checklist con {len(tasks) if not existing_template else 'tasks esistenti'}")

except Exception as e:
    print(f"❌ Errore durante l'inizializzazione: {e}")
    db.rollback()
    raise

finally:
    db.close()



