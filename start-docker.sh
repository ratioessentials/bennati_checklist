#!/bin/bash

echo "🏠 Bennati Checklist - Avvio Docker"
echo "===================================="
echo ""

# Ferma eventuali container esistenti
echo "🛑 Fermando container esistenti..."
docker-compose down

echo ""
echo "🐳 Avvio container Docker..."
docker-compose up -d --build

echo ""
echo "⏳ Attendo che il database sia pronto..."
sleep 10

echo ""
echo "🌱 Inizializzazione database con dati di esempio..."
docker-compose exec -T backend python init_data.py

echo ""
echo "✅ Setup completato!"
echo ""
echo "🌐 L'applicazione è disponibile su:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Credenziali di test:"
echo "   - Nome operatore: Maria (o qualsiasi nome)"
echo "   - Nome manager: Manager"
echo "   - Appartamenti: 1, 2, 3, 4"
echo ""
echo "📊 Per vedere i logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Per fermare l'applicazione:"
echo "   docker-compose down"
echo ""

