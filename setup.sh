#!/bin/bash

# Script di setup automatico per Bennati Checklist
# Uso: ./setup.sh

set -e  # Exit on error

echo "🏠 Bennati Checklist - Setup Automatico"
echo "========================================"
echo ""

# Controlla prerequisiti
echo "📋 Controllo prerequisiti..."

# Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato. Installalo da python.org"
    exit 1
fi
echo "✅ Python 3 trovato: $(python3 --version)"

# Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js non trovato. Installalo da nodejs.org"
    exit 1
fi
echo "✅ Node.js trovato: $(node --version)"

# PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL non trovato. Installalo da postgresql.org"
    exit 1
fi
echo "✅ PostgreSQL trovato: $(psql --version)"

echo ""
echo "📦 Setup Backend..."
cd backend

# Virtual environment
if [ ! -d "venv" ]; then
    echo "Creazione virtual environment..."
    python3 -m venv venv
fi

# Attiva venv
source venv/bin/activate

# Installa dipendenze
echo "Installazione dipendenze Python..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Configura .env se non esiste
if [ ! -f ".env" ]; then
    echo "Creazione file .env..."
    cp .env.example .env
    
    # Genera secret key casuale
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    # macOS usa sed diversamente da Linux
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/your-secret-key-change-this-in-production/$SECRET_KEY/" .env
    else
        sed -i "s/your-secret-key-change-this-in-production/$SECRET_KEY/" .env
    fi
    
    echo "⚠️  IMPORTANTE: Modifica backend/.env con le credenziali PostgreSQL corrette!"
fi

# Crea directory uploads
mkdir -p uploads

echo "✅ Backend setup completato"
cd ..

echo ""
echo "🎨 Setup Frontend..."
cd frontend

# Installa dipendenze
echo "Installazione dipendenze Node.js..."
npm install --silent

# Configura .env se non esiste
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

echo "✅ Frontend setup completato"
cd ..

echo ""
echo "🗄️  Setup Database..."

# Chiedi credenziali database
echo "Inserisci le credenziali PostgreSQL:"
read -p "Username [postgres]: " DB_USER
DB_USER=${DB_USER:-postgres}

read -sp "Password: " DB_PASSWORD
echo ""

read -p "Host [localhost]: " DB_HOST
DB_HOST=${DB_HOST:-localhost}

read -p "Port [5432]: " DB_PORT
DB_PORT=${DB_PORT:-5432}

# Verifica connessione
if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c "SELECT 1" &> /dev/null; then
    echo "✅ Connessione database OK"
else
    echo "❌ Impossibile connettersi al database. Verifica le credenziali."
    exit 1
fi

# Crea database
echo "Creazione database bennati_checklist..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c "CREATE DATABASE bennati_checklist;" 2>/dev/null || echo "Database già esistente, skip..."

# Aggiorna .env con credenziali
DATABASE_URL="postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/bennati_checklist"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s|DATABASE_URL=.*|DATABASE_URL=$DATABASE_URL|" backend/.env
else
    sed -i "s|DATABASE_URL=.*|DATABASE_URL=$DATABASE_URL|" backend/.env
fi

echo "✅ Database configurato"

echo ""
echo "🌱 Inizializzazione dati..."
cd backend
source venv/bin/activate
python init_data.py
cd ..

echo ""
echo "🎉 Setup completato con successo!"
echo ""
echo "Per avviare l'applicazione:"
echo ""
echo "1️⃣  Backend (terminale 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "2️⃣  Frontend (terminale 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3️⃣  Apri browser:"
echo "   http://localhost:3000"
echo ""
echo "📚 Leggi QUICKSTART.md per iniziare!"
echo ""



