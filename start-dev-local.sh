#!/bin/bash

echo "🚀 Avvio Bennati Checklist in Development Mode (Locale)"
echo "======================================================"

# Ferma i container di produzione se sono in esecuzione
echo "🛑 Fermando container di produzione..."
docker-compose down

# Avvia solo il database
echo "🗄️ Avviando database PostgreSQL..."
docker-compose -f docker-compose.dev.yml up -d db

# Attendi che il database sia pronto
echo "⏳ Attendendo che il database sia pronto..."
sleep 5

# Inizializza il database se necessario
echo "🔧 Inizializzando database..."
docker-compose -f docker-compose.dev.yml exec -T db psql -U bennati -d bennati_checklist -c "SELECT 1;" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "📊 Creando database e tabelle..."
    docker-compose -f docker-compose.dev.yml exec -T db psql -U bennati -c "CREATE DATABASE bennati_checklist;" 2>/dev/null || true
fi

echo ""
echo "✅ Development environment avviato!"
echo ""
echo "🗄️ Database: localhost:5433"
echo ""
echo "🔧 Per avviare backend e frontend localmente:"
echo ""
echo "Backend (in una nuova finestra terminale):"
echo "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Frontend (in una nuova finestra terminale):"
echo "cd frontend && npm run dev"
echo ""
echo "🌐 Poi apri: http://localhost:5173"
echo ""
echo "🛑 Per fermare: docker-compose -f docker-compose.dev.yml down"
