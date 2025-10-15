from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from database import get_db, engine
from models import Base, User, Apartment, Checklist, Task
from schemas import (
    LoginRequest, LoginResponse, User as UserSchema, 
    Apartment as ApartmentSchema, Checklist as ChecklistSchema,
    ChecklistCreate, Task as TaskSchema
)
from auth import verify_password, create_access_token, verify_token

load_dotenv()

# Crea tabelle
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Checklist API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token non valido"
        )
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utente non trovato"
        )
    return user

@app.get("/")
def read_root():
    return {"message": "Checklist API is running!"}

@app.post("/api/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o password non validi"
        )
    
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=timedelta(minutes=30)
    )
    
    return LoginResponse(
        success=True,
        message="Login riuscito!",
        user=UserSchema.from_orm(user),
        token=access_token
    )

@app.get("/api/apartments", response_model=list[ApartmentSchema])
def get_apartments(db: Session = Depends(get_db)):
    return db.query(Apartment).all()

@app.post("/api/checklists", response_model=ChecklistSchema)
def create_checklist(
    checklist_data: ChecklistCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    checklist = Checklist(
        user_id=current_user.id,
        apartment_id=checklist_data.apartment_id,
        notes=checklist_data.notes
    )
    db.add(checklist)
    db.commit()
    db.refresh(checklist)
    
    # Crea task standard per la checklist
    standard_tasks = [
        "Aspirare/lavare pavimenti",
        "Pulire bagno completo", 
        "Cambiare biancheria letto",
        "Pulire cucina e fornelli",
        "Svuotare cestini",
        "Rifornire consumabili (carta, sapone, ecc.)",
        "Controllo inventario completato",
        "Foto dello stato finale",
        "Note aggiuntive o problemi riscontrati"
    ]
    
    for i, task_desc in enumerate(standard_tasks):
        task = Task(
            checklist_id=checklist.id,
            description=task_desc,
            order_index=i
        )
        db.add(task)
    
    db.commit()
    db.refresh(checklist)
    return checklist

@app.get("/api/checklists", response_model=list[ChecklistSchema])
def get_checklists(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Checklist).filter(Checklist.user_id == current_user.id).all()

@app.get("/api/checklists/{checklist_id}", response_model=ChecklistSchema)
def get_checklist(
    checklist_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    checklist = db.query(Checklist).filter(
        Checklist.id == checklist_id,
        Checklist.user_id == current_user.id
    ).first()
    
    if not checklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist non trovata"
        )
    
    return checklist

@app.patch("/api/tasks/{task_id}/complete")
def complete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).join(Checklist).filter(
        Task.id == task_id,
        Checklist.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task non trovato"
        )
    
    task.completed = True
    db.commit()
    
    return {"message": "Task completato"}

@app.patch("/api/checklists/{checklist_id}/complete")
def complete_checklist(
    checklist_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    checklist = db.query(Checklist).filter(
        Checklist.id == checklist_id,
        Checklist.user_id == current_user.id
    ).first()
    
    if not checklist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checklist non trovata"
        )
    
    checklist.completed = True
    checklist.completed_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Checklist completata"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
