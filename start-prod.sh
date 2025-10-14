#!/bin/bash

echo "🚀 Avvio Bennati Checklist in Production Mode"
echo "============================================="

# Ferma i container di development se sono in esecuzione
echo "🛑 Fermando container di development..."
docker-compose -f docker-compose.dev.yml down

# Avvia i container di produzione
echo "🏭 Avviando container di produzione..."
docker-compose up -d --build

echo ""
echo "✅ Production environment avviato!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 Database: localhost:5433"
echo ""
echo "🛑 Per fermare: docker-compose down"
