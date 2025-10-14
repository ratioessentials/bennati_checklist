#!/bin/bash

echo "🚀 Avvio Bennati Checklist in Development Mode"
echo "=============================================="

# Ferma i container di produzione se sono in esecuzione
echo "🛑 Fermando container di produzione..."
docker-compose down

# Avvia i container di development
echo "🔧 Avviando container di development..."
docker-compose -f docker-compose.dev.yml up -d --build

echo ""
echo "✅ Development environment avviato!"
echo ""
echo "🌐 Frontend (con hot reload): http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 Database: localhost:5433"
echo ""
echo "💡 Modifica i file e vedi le modifiche in tempo reale!"
echo "🛑 Per fermare: docker-compose -f docker-compose.dev.yml down"
