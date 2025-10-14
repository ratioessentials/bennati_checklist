from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from database import engine, Base
from routers import users, apartments, checklists, inventory, reports

load_dotenv()

# Crea tabelle database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bennati Checklist API",
    description="API per gestione checklist pulizie appartamenti",
    version="1.0.0"
)

# CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(users.router)
app.include_router(apartments.router)
app.include_router(checklists.router)
app.include_router(inventory.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {
        "message": "Bennati Checklist API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



