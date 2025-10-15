from database import engine, SessionLocal
from models import Base, User, Apartment, Task, Checklist
from auth import hash_password

# Crea tutte le tabelle
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Crea utenti
    users_data = [
        {"username": "sofia", "name": "Sofia", "password": "Prova123!"},
        {"username": "giulia", "name": "Giulia", "password": "Prova123!"},
        {"username": "martina", "name": "Martina", "password": "Prova123!"},
        {"username": "chiara", "name": "Chiara", "password": "Prova123!"},
        {"username": "admin", "name": "Amministratore", "password": "admin123"}
    ]
    
    for user_data in users_data:
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if not existing:
            user = User(
                username=user_data["username"],
                password_hash=hash_password(user_data["password"]),
                name=user_data["name"]
            )
            db.add(user)
    
    # Crea appartamenti
    apartments_data = [
        {"name": "Monolocale", "description": "Monolocale, cucina e bagno"},
        {"name": "Bilocale 1°", "description": "Primo piano, 2 camere"},
        {"name": "Bilocale Terra", "description": "Piano terra, 2 camere"},
        {"name": "Trilocale", "description": "3 camere, cucina e bagno"}
    ]
    
    for apt_data in apartments_data:
        existing = db.query(Apartment).filter(Apartment.name == apt_data["name"]).first()
        if not existing:
            apartment = Apartment(**apt_data)
            db.add(apartment)
    
    db.commit()
    print("✅ Database inizializzato con successo!")
    print("   - 5 utenti creati")
    print("   - 4 appartamenti creati")
    print("\n🔑 Credenziali di test:")
    print("   Username: sofia, giulia, martina, chiara, admin")
    print("   Password: Prova123! (admin: admin123)")

except Exception as e:
    print(f"❌ Errore: {e}")
    db.rollback()
finally:
    db.close()
