# 🐳 Guida Docker - Bennati Checklist

## 🚀 Avvio Rapido

### Opzione 1: Script Automatico (Consigliato)

```bash
cd /Users/joshmini/Desktop/bennati_checklist
./start-docker.sh
```

Lo script farà tutto automaticamente:
- ✅ Ferma container esistenti
- ✅ Avvia PostgreSQL, Backend e Frontend
- ✅ Aspetta che il database sia pronto
- ✅ Inizializza dati di esempio

### Opzione 2: Comandi Manuali

```bash
cd /Users/joshmini/Desktop/bennati_checklist

# Avvia tutti i servizi
docker-compose up -d --build

# Aspetta 10 secondi che il database sia pronto
sleep 10

# Inizializza database
docker-compose exec backend python init_data.py
```

## 🌐 Accesso all'Applicazione

Dopo l'avvio, l'app sarà disponibile su:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

## 📝 Credenziali di Test

**Login Operatore:**
- Nome: `Maria` (o qualsiasi nome)
- Appartamento: Seleziona tra Monolocale, Bilocale 1°, Bilocale Terra, Trilocale
- Data: Oggi

**Login Manager:**
- Nome: `Manager`
- Appartamento: Qualsiasi
- Data: Oggi

## 🔍 Comandi Utili

### Vedere i logs

```bash
# Tutti i servizi
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend

# Solo database
docker-compose logs -f db
```

### Fermare i container

```bash
# Ferma tutti i container
docker-compose down

# Ferma e rimuovi anche i volumi (ATTENZIONE: cancella il database!)
docker-compose down -v
```

### Riavviare un servizio

```bash
# Riavvia solo il backend
docker-compose restart backend

# Riavvia solo il frontend
docker-compose restart frontend
```

### Accedere a un container

```bash
# Accedi al backend
docker-compose exec backend bash

# Accedi al database
docker-compose exec db psql -U bennati -d bennati_checklist
```

### Vedere stato dei container

```bash
docker-compose ps
```

### Reinizializzare il database

```bash
# ATTENZIONE: Questo cancella tutti i dati!
docker-compose down -v
docker-compose up -d
sleep 10
docker-compose exec backend python init_data.py
```

## 🛠️ Troubleshooting

### Problema: "Port already in use"

**Errore**: `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Soluzione**:
```bash
# Trova processo che usa la porta
lsof -i :3000  # o :8000, :5432

# Ferma il processo
kill -9 PID

# Oppure cambia porta in docker-compose.yml
```

### Problema: Database non si connette

**Errore**: `could not connect to server`

**Soluzione**:
```bash
# Controlla che il container db sia in running
docker-compose ps

# Riavvia il database
docker-compose restart db

# Aspetta qualche secondo e riprova
```

### Problema: "No such file or directory" durante init_data.py

**Soluzione**:
```bash
# Ricostruisci i container
docker-compose down
docker-compose up -d --build
sleep 10
docker-compose exec backend python init_data.py
```

### Problema: Frontend non si connette al backend

**Soluzione**:
```bash
# Verifica che tutti i servizi siano in running
docker-compose ps

# Controlla i logs del backend
docker-compose logs backend

# Riavvia il frontend
docker-compose restart frontend
```

### Problema: Modifiche al codice non si vedono

**Soluzione**:
```bash
# Per il backend/frontend in sviluppo, i volumi montano il codice
# quindi le modifiche dovrebbero essere immediate

# Se non funziona, ricostruisci:
docker-compose down
docker-compose up -d --build
```

## 📦 Servizi Docker

### Database (PostgreSQL)
- **Image**: postgres:14-alpine
- **Porta**: 5432
- **User**: bennati
- **Password**: bennati_password
- **Database**: bennati_checklist
- **Volume**: postgres_data (persistente)

### Backend (FastAPI)
- **Porta**: 8000
- **Volume**: ./backend → /app (live reload)
- **Volume**: backend_uploads (persistente)
- **Dipende**: db

### Frontend (React + Vite)
- **Porta**: 3000
- **Volume**: ./frontend → /app (live reload)
- **Dipende**: backend

## 🔄 Sviluppo con Docker

### Hot Reload

Entrambi backend e frontend hanno hot reload attivo:

**Backend**: Uvicorn con `--reload`
**Frontend**: Vite con `--host`

Modifica i file localmente e i cambiamenti si vedranno automaticamente!

### Aggiungere dipendenze

**Backend:**
```bash
# Aggiungi a requirements.txt
echo "nuova-libreria==1.0.0" >> backend/requirements.txt

# Ricostruisci
docker-compose up -d --build backend
```

**Frontend:**
```bash
# Accedi al container
docker-compose exec frontend npm install nuova-libreria

# Oppure rebuilda
docker-compose up -d --build frontend
```

### Eseguire comandi custom

```bash
# Backend: Crea migration Alembic
docker-compose exec backend alembic revision --autogenerate -m "descrizione"

# Frontend: Run tests
docker-compose exec frontend npm test

# Database: Backup
docker-compose exec db pg_dump -U bennati bennati_checklist > backup.sql
```

## 📊 Monitoraggio

### Resource Usage

```bash
# Mostra uso CPU/RAM
docker stats

# Solo per i nostri container
docker stats bennati_backend bennati_frontend bennati_db
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000

# Database
docker-compose exec db pg_isready -U bennati
```

## 🚢 Preparare per Produzione

Il `docker-compose.yml` attuale è per **sviluppo**. Per produzione:

1. **Rimuovi volumi source code**
2. **Usa build ottimizzato frontend** (npm run build)
3. **Aggiungi Nginx** per servire frontend
4. **Usa variabili ambiente per secrets**
5. **Setup SSL/HTTPS**
6. **Aggiungi health checks**
7. **Setup backup automatici**

Esempio docker-compose.prod.yml da creare separatamente.

## 🎯 Best Practices

1. **Non committare .env** con password reali
2. **Backup database** prima di `docker-compose down -v`
3. **Usa tags specifici** per immagini (non latest)
4. **Monitora logs** regolarmente
5. **Limita risorse** container in produzione

## 💡 Tips

- **Ctrl+C** nei logs ferma il follow, non i container
- **docker-compose down** preserva i volumi (database)
- **docker-compose down -v** cancella TUTTO (attenzione!)
- I file in `uploads/` sono persistenti nel volume `backend_uploads`
- Modifica `.env` e poi `docker-compose restart` per applicare

---

**Buon sviluppo! 🐳**

