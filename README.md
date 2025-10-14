# 🏠 Bennati Checklist - Sistema Gestione Pulizie Appartamenti

Sistema completo per la gestione delle pulizie, inventario e reportistica per 4 appartamenti. Mobile-first design ottimizzato per smartphone.

## 📋 Caratteristiche Principali

### ✅ Gestione Operatori
- Login con selezione nome operatore, data e appartamento
- Tracciamento completo delle attività per operatore
- Sistema di autenticazione con token JWT

### 📝 Checklist Dinamiche
- Checklist personalizzabili per ogni appartamento
- Task di diversi tipi:
  - Checkbox (completamento semplice)
  - Testo libero (note e descrizioni)
  - Sì/No (domande verifiche)
  - Upload foto/video (documentazione visiva)
- Salvataggio automatico progressi
- Validazione task obbligatorie

### 📦 Inventario Intelligente
- Gestione articoli per categoria (Cucina, Bagno, Camera, Consumabili, Pulizia)
- Controllo quantità in tempo reale
- Soglie minime personalizzabili
- Alert automatici per scorte basse
- Storico modifiche inventario

### 📊 Dashboard Manageriale
- Panoramica completa tutti gli appartamenti
- Alert attivi e prioritizzati
- Lista articoli da riordinare
- Statistiche checklist completate
- Export report (PDF/CSV)

### 🔔 Sistema Alert
- Notifiche automatiche per scorte basse
- Alert per articoli mancanti (quantità = 0)
- Classificazione per priorità (low/medium/high)

## 🏗️ Architettura

### Backend (FastAPI + PostgreSQL)
```
backend/
├── main.py              # Entry point FastAPI
├── database.py          # Configurazione database
├── models.py            # Modelli SQLAlchemy
├── schemas.py           # Schemi Pydantic
├── auth.py              # Autenticazione JWT
├── init_data.py         # Script inizializzazione dati
├── routers/
│   ├── users.py         # API utenti e login
│   ├── apartments.py    # API appartamenti
│   ├── checklists.py    # API checklist e task
│   ├── inventory.py     # API inventario
│   └── reports.py       # API reportistica
└── requirements.txt     # Dipendenze Python
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── main.jsx              # Entry point React
│   ├── App.jsx               # Router principale
│   ├── index.css             # Stili globali
│   ├── context/
│   │   └── AppContext.jsx    # State management globale
│   ├── services/
│   │   └── api.js            # Client API
│   ├── components/
│   │   └── Layout.jsx        # Layout principale
│   └── pages/
│       ├── LoginPage.jsx           # Login operatori
│       ├── ChecklistPage.jsx       # Gestione checklist
│       ├── InventoryPage.jsx       # Gestione inventario
│       └── ManagerDashboard.jsx    # Dashboard manager
├── index.html
├── vite.config.js
└── package.json
```

## 🚀 Installazione e Setup

### Prerequisiti
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+

### 1. Setup Database

```bash
# Crea database PostgreSQL
createdb bennati_checklist

# Oppure via psql
psql -U postgres
CREATE DATABASE bennati_checklist;
```

### 2. Setup Backend

```bash
cd backend

# Crea virtual environment
python -m venv venv

# Attiva virtual environment
# Su macOS/Linux:
source venv/bin/activate
# Su Windows:
# venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt

# Configura variabili ambiente
cp .env.example .env
# Modifica .env con le tue credenziali database

# Inizializza database con dati di esempio
python init_data.py

# Avvia server
python main.py
```

Il backend sarà disponibile su: http://localhost:8000
Documentazione API: http://localhost:8000/docs

### 3. Setup Frontend

```bash
cd frontend

# Installa dipendenze
npm install

# Avvia server di sviluppo
npm run dev
```

Il frontend sarà disponibile su: http://localhost:3000

## 🔧 Configurazione

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/bennati_checklist
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
UPLOAD_DIR=./uploads
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend
Le variabili d'ambiente del frontend possono essere configurate in un file `.env`:
```env
VITE_API_URL=http://localhost:8000
```

## 📱 Utilizzo

### Per Operatori

1. **Login**
   - Apri l'app su smartphone
   - Inserisci nome
   - Seleziona appartamento
   - Scegli data (default: oggi)
   - Click "Inizia Turno"

2. **Checklist**
   - Completa tutte le task obbligatorie (*)
   - Carica foto dove richiesto
   - Aggiungi note aggiuntive
   - Click "Completa Checklist"

3. **Inventario**
   - Verifica quantità articoli
   - Aggiorna quantità con +/-
   - Usa filtri per categoria
   - Click "Salva Modifiche"

### Per Manager

1. **Dashboard**
   - Visualizza overview tutti gli appartamenti
   - Monitora alert attivi
   - Controlla articoli da riordinare
   - Esporta report PDF/CSV

2. **Report**
   - Export globale (tutti appartamenti)
   - Export per singolo appartamento
   - Statistiche completamento checklist

## 🗄️ Modello Dati

### Entità Principali

- **User**: Operatori e manager
- **Apartment**: 4 appartamenti
- **Checklist**: Sessione pulizia
- **TaskResponse**: Risposta a task checklist
- **InventoryItem**: Articolo inventario
- **Alert**: Notifiche scorte basse

### Relazioni
- Un User può avere molte Checklist
- Un Apartment ha molte Checklist e InventoryItem
- Una Checklist ha molte TaskResponse
- Ogni InventoryItem traccia storico modifiche

## 🎨 Design Mobile-First

### Caratteristiche UX
- Touch targets minimi 44px
- Font size minimo 16px (no zoom su iOS)
- Layout responsive e ottimizzato per portrait
- Sticky header e navigation
- Bottom action bar per azioni principali
- Swipe gestures friendly
- Ottimizzato per connessioni lente

### Browser Supportati
- Safari iOS 14+
- Chrome Android 80+
- Chrome/Firefox/Safari Desktop (ultimi 2 versioni)

## 📊 API Endpoints Principali

### Autenticazione
- `POST /api/users/login` - Login operatore

### Checklist
- `GET /api/checklists/` - Lista checklist
- `GET /api/checklists/{id}` - Dettaglio checklist
- `PUT /api/checklists/{id}` - Aggiorna checklist
- `PUT /api/checklists/tasks/{id}` - Aggiorna task
- `POST /api/checklists/tasks/{id}/upload` - Upload foto

### Inventario
- `GET /api/inventory/items` - Lista articoli
- `PUT /api/inventory/items/{id}` - Aggiorna quantità
- `GET /api/inventory/alerts` - Lista alert

### Report
- `GET /api/reports/dashboard` - Dashboard manager
- `GET /api/reports/export/inventory/pdf` - Export PDF
- `GET /api/reports/export/inventory/csv` - Export CSV

## 🔐 Sicurezza

- Autenticazione JWT con token
- CORS configurabile
- Validazione input con Pydantic
- SQL injection protection (SQLAlchemy ORM)
- File upload validation (tipo e dimensione)

## 🚀 Deployment Produzione

### Backend
```bash
# Usa un server WSGI production-ready
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
npm run build
# Deploy cartella dist/ su server static (Nginx, Apache, Vercel, Netlify)
```

### Database
- Configura backup automatici PostgreSQL
- Usa connection pooling
- Implementa migrazioni con Alembic

### Raccomandazioni
- Usa HTTPS (Let's Encrypt)
- Configura rate limiting
- Monitora con Sentry/LogRocket
- Backup giornalieri database
- CDN per assets statici

## 🌐 Funzionalità Opzionali (Bonus)

### Implementate
- ✅ Sistema ruoli (operatore/manager)
- ✅ Upload foto/video
- ✅ Export PDF/CSV
- ✅ Storico inventario
- ✅ Alert automatici
- ✅ Statistiche appartamenti

### Da Implementare
- ⏳ Multilingua (IT/EN)
- ⏳ Notifiche push
- ⏳ Calendario interventi
- ⏳ QR code appartamenti
- ⏳ Stampa diretta checklist

## 🐛 Troubleshooting

### Backend non si avvia
```bash
# Verifica database
psql -d bennati_checklist -c "SELECT 1;"

# Verifica dipendenze
pip install -r requirements.txt --upgrade

# Check logs
tail -f logs/app.log
```

### Frontend non si connette al backend
- Verifica CORS in backend/.env
- Controlla che backend sia su porta 8000
- Verifica proxy in vite.config.js

### Upload foto non funziona
- Verifica permessi cartella uploads/
- Check dimensione file (max 10MB)
- Verifica UPLOAD_DIR in .env

## 📞 Supporto

Per problemi o domande:
- Email: support@bennati-checklist.com
- Issues: GitHub repository

## 📄 Licenza

Proprietario - Bennati Pulizie © 2025

## 👥 Credits

Sviluppato con:
- FastAPI - Framework backend
- React - Framework frontend
- PostgreSQL - Database
- Lucide React - Icons
- React Toastify - Notifications
- ReportLab - PDF generation

---

**Versione**: 1.0.0  
**Ultimo aggiornamento**: Ottobre 2025  
**Compatibilità**: Mobile First (iOS/Android)



