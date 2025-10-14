#!/bin/bash

echo "🚀 Avvio Bennati Checklist in Development Mode (Semplificato)"
echo "============================================================"

# Ferma i container esistenti
echo "🛑 Fermando container esistenti..."
docker-compose down
docker-compose -f docker-compose.dev.yml down

# Avvia solo il database
echo "🗄️ Avviando database PostgreSQL..."
docker-compose -f docker-compose.dev.yml up -d db

# Attendi che il database sia pronto
echo "⏳ Attendendo che il database sia pronto..."
sleep 8

# Inizializza il database
echo "🔧 Inizializzando database..."
docker-compose -f docker-compose.dev.yml exec -T db psql -U bennati -d bennati_checklist -c "SELECT 1;" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "📊 Creando database e tabelle..."
    docker-compose -f docker-compose.dev.yml exec -T db psql -U bennati -c "CREATE DATABASE bennati_checklist;" 2>/dev/null || true
    sleep 2
fi

echo ""
echo "✅ Database pronto!"
echo ""
echo "🔧 Ora avvia backend e frontend:"
echo ""
echo "1️⃣ Backend (nuova finestra terminale):"
echo "   cd backend"
echo "   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2️⃣ Frontend (nuova finestra terminale):"
echo "   cd frontend" 
echo "   npm run dev"
echo ""
echo "🌐 Poi apri: http://localhost:5173"
echo ""
echo "💡 Modifica i file e vedi le modifiche in tempo reale!"
echo "🛑 Per fermare: docker-compose -f docker-compose.dev.yml down"
