# 🔧 Guida Development

## 🚀 Avvio Rapido Development

### Opzione A: Development Semplificato (Consigliato)

```bash
# 1. Avvia solo il database
./start-dev-simple.sh

# 2. In una nuova finestra terminale - Backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 3. In una nuova finestra terminale - Frontend  
cd frontend
npm run dev

# 4. Apri il browser
open http://localhost:5173
```

### Opzione B: Development Completo Docker

```bash
# Avvia tutto con Docker
./start-dev.sh

# Apri il browser
open http://localhost:5173
```

## 📁 Struttura Development

```
bennati_checklist/
├── backend/                 # API FastAPI
│   ├── main.py             # Entry point
│   ├── models.py           # Modelli database
│   ├── routers/            # Endpoint API
│   └── requirements.txt    # Dipendenze Python
├── frontend/               # App React
│   ├── src/
│   │   ├── components/     # Componenti React
│   │   ├── pages/          # Pagine
│   │   └── services/       # Client API
│   └── package.json        # Dipendenze Node.js
└── docker-compose.dev.yml  # Configurazione development
```

## 🔄 Hot Reload

### Frontend (React + Vite)
- ✅ **Modifica file JSX/CSS** → Ricarica automatica
- ✅ **Modifica componenti** → Hot reload istantaneo
- ✅ **Modifica stili** → Aggiornamento live

### Backend (FastAPI + Uvicorn)
- ✅ **Modifica file Python** → Ricarica automatica
- ✅ **Modifica API** → Restart automatico
- ✅ **Modifica modelli** → Ricarica server

## 🛠️ Comandi Utili

### Database
```bash
# Connessione diretta al database
docker-compose -f docker-compose.dev.yml exec db psql -U bennati -d bennati_checklist

# Reset database
docker-compose -f docker-compose.dev.yml down -v
./start-dev-simple.sh
```

### Backend
```bash
# Avvia backend con debug
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

# Installa nuove dipendenze
pip install nuova-dipendenza
# Aggiungi a requirements.txt
```

### Frontend
```bash
# Avvia frontend con debug
cd frontend
npm run dev -- --debug

# Installa nuove dipendenze
npm install nuova-dipendenza
```

## 🐛 Debug

### Backend
- **Log**: Visibili nel terminale dove avvii uvicorn
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5433

### Frontend  
- **DevTools**: F12 nel browser
- **Console**: Errori JavaScript visibili
- **Network**: Richieste API in Network tab

## 📊 Porte Development

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **Database**: localhost:5433
- **API Docs**: http://localhost:8000/docs

## 🔧 Troubleshooting

### Database non si connette
```bash
# Riavvia database
docker-compose -f docker-compose.dev.yml restart db
```

### Backend non si avvia
```bash
# Installa dipendenze
cd backend
pip install -r requirements.txt
```

### Frontend non si avvia
```bash
# Installa dipendenze
cd frontend
npm install
```

### Porte occupate
```bash
# Trova processo che usa la porta
lsof -i :8000  # Backend
lsof -i :5173  # Frontend
lsof -i :5433  # Database

# Termina processo
kill -9 <PID>
```

## 🚀 Deploy Development

### Test Locale
```bash
# Avvia tutto in development
./start-dev-simple.sh

# Testa tutte le funzionalità
# - Login operatore
# - Checklist
# - Inventario  
# - Dashboard manager
```

### Build Produzione
```bash
# Testa build produzione
./start-prod.sh

# Verifica che tutto funzioni
open http://localhost:3000
```

## 💡 Tips Development

1. **Usa il Development Semplificato** per modifiche frequenti
2. **Modifica un file alla volta** per debug più facile
3. **Controlla i log** nel terminale per errori
4. **Usa le DevTools** del browser per debug frontend
5. **Testa su mobile** con le dimensioni simulate
