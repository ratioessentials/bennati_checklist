"""
Passenger WSGI file per deployment su Plesk
Questo file viene usato da Passenger per servire l'app FastAPI
"""
import sys
import os

# Aggiungi il path della directory backend
sys.path.insert(0, os.path.dirname(__file__))

# Carica variabili ambiente dal file .env
from dotenv import load_dotenv
load_dotenv()

# Import dell'app FastAPI
from main import app

# L'applicazione WSGI che Passenger userà
application = app

# Per debug (rimuovi in produzione)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

