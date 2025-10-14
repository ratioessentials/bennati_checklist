# Changelog

Tutte le modifiche notevoli a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce a [Semantic Versioning](https://semver.org/lang/it/).

## [1.0.0] - 2025-10-13

### 🎉 Release Iniziale

#### ✨ Funzionalità Aggiunte

**Autenticazione e Utenti**
- Sistema di login operatori con selezione appartamento e data
- Gestione ruoli (operatore/manager)
- Autenticazione JWT con token
- Tracciamento utente per ogni attività

**Checklist Dinamiche**
- Template checklist personalizzabili per appartamento
- Task di tipo: checkbox, testo libero, sì/no, upload foto/video
- Validazione task obbligatorie
- Salvataggio progressi in tempo reale
- Note aggiuntive per ogni checklist
- Upload foto/video fino a 10MB
- Storico completo checklist completate

**Gestione Inventario**
- Categorie inventario: Cucina, Bagno, Camera, Consumabili, Pulizia
- Articoli configurabili con quantità e soglie minime
- Aggiornamento quantità in tempo reale con +/-
- Storico modifiche inventario con tracciamento utente
- Filtri per categoria e scorte basse
- Ricerca articoli

**Sistema Alert**
- Alert automatici per scorte ≤ minimo
- Classificazione severità (low/medium/high)
- Alert per articoli mancanti (quantità = 0)
- Pannello alert per manager
- Risoluzione alert tracciata

**Dashboard Manageriale**
- Overview tutti gli appartamenti
- Statistiche checklist (totali, completate, tasso completamento)
- Lista articoli da riordinare
- Alert attivi con priorità
- Visualizzazione scorte per appartamento
- Statistiche ultimi 30 giorni

**Reportistica**
- Export inventario in PDF
- Export inventario in CSV
- Export checklist in CSV
- Report per appartamento o globale
- Statistiche dettagliate per appartamento

**Design e UX**
- Mobile-first responsive design
- Touch targets ottimizzati (44px minimum)
- Sticky header e navigation
- Bottom action buttons
- Loading states e feedback visivo
- Toast notifications
- Interfaccia in italiano
- Icone Lucide React

**Infrastruttura**
- Backend FastAPI con documentazione OpenAPI
- Frontend React con Vite
- Database PostgreSQL con SQLAlchemy ORM
- CORS configurabile
- Upload files con validazione
- Docker support completo
- Script setup automatico

#### 📚 Documentazione
- README completo con guida installazione
- QUICKSTART per setup rapido
- ARCHITETTURA tecnica dettagliata
- FAQ con domande comuni
- CONTRIBUIRE per sviluppatori
- Commenti inline nel codice

#### 🛠️ Sviluppo
- Struttura progetto modulare
- Separazione backend/frontend
- Environment variables per configurazione
- Logging strutturato
- Error handling robusto
- Validazione input con Pydantic

#### 🔒 Sicurezza
- JWT authentication
- SQL injection protection (ORM)
- File upload validation
- CORS configurabile
- Input sanitization
- XSS protection (React)

#### 🎨 Design System
- Palette colori consistente
- Componenti riutilizzabili
- CSS variables
- Utility classes
- Responsive breakpoints
- Dark mode ready (base)

### 📦 Dipendenze

**Backend:**
- FastAPI 0.109.0
- SQLAlchemy 2.0.25
- PostgreSQL 14+
- Python 3.9+

**Frontend:**
- React 18.2.0
- Vite 5.0.8
- Axios 1.6.2
- React Router 6.21.0
- Lucide React 0.294.0

### 🐛 Bug Conosciuti
Nessuno al momento della release.

### ⚠️ Breaking Changes
N/A - Prima release

### 🔄 Migrazioni
N/A - Prima release

---

## [Unreleased]

### Pianificato per v1.1.0
- [ ] Multilingua (Italiano/Inglese)
- [ ] Notifiche push
- [ ] PWA completo con offline support
- [ ] Calendario interventi
- [ ] QR code appartamenti
- [ ] Stampa diretta checklist
- [ ] Dashboard analytics avanzata
- [ ] Esportazione PDF con grafici

### In Valutazione
- [ ] App mobile nativa (React Native)
- [ ] Integrazione calendario Google/Outlook
- [ ] Sistema prenotazioni pulizie
- [ ] Chat interna team
- [ ] Gestione turni automatica
- [ ] OCR per documenti
- [ ] Firma digitale checklist

---

## Come Aggiornare

### Da v1.0.0 a v1.1.0 (futuro)
```bash
# Backup database
pg_dump bennati_checklist > backup.sql

# Update codice
git pull origin main

# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt --upgrade
alembic upgrade head

# Frontend
cd ../frontend
npm install
npm run build

# Restart services
```

---

## Note di Versione

### Versione Semantica
- **MAJOR**: Breaking changes
- **MINOR**: Nuove funzionalità compatibili
- **PATCH**: Bug fixes

### Support Policy
- **v1.x**: Supportato con bug fixes e security patches
- **v0.x**: Non più supportato dopo release v1.0.0

---

**Per dettagli completi**: Vedi [commit history](https://github.com/bennati/commits) su GitHub



