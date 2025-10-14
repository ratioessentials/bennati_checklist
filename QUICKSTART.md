# 🚀 Quick Start Guide - Bennati Checklist

Guida rapida per avviare l'applicazione in 5 minuti.

## Opzione 1: Docker (Più Semplice) 🐳

### Prerequisiti
- Docker Desktop installato
- Docker Compose installato

### Avvio
```bash
# Clona o vai nella directory del progetto
cd bennati_checklist

# Avvia tutti i servizi
docker-compose up -d

# Inizializza database con dati di esempio
docker-compose exec backend python init_data.py

# Verifica che tutto funzioni
docker-compose ps
```

✅ **Fatto!** L'app è ora disponibile su:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Ferma i servizi
```bash
docker-compose down
```

### Reset completo
```bash
docker-compose down -v  # Elimina anche i volumi (database)
docker-compose up -d
docker-compose exec backend python init_data.py
```

---

## Opzione 2: Installazione Manuale 🛠️

### Prerequisiti
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+

### 1️⃣ Setup Database (5 minuti)

```bash
# Crea database
createdb bennati_checklist

# O via psql
psql -U postgres
# Poi esegui:
CREATE DATABASE bennati_checklist;
\q
```

### 2️⃣ Setup Backend (5 minuti)

```bash
cd backend

# Crea ambiente virtuale
python -m venv venv

# Attiva ambiente
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt

# Configura variabili ambiente
cat > .env << EOF
DATABASE_URL=postgresql://postgres:password@localhost:5432/bennati_checklist
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
UPLOAD_DIR=./uploads
CORS_ORIGINS=http://localhost:3000
EOF

# ⚠️ IMPORTANTE: Modifica .env con la password corretta di PostgreSQL!

# Inizializza database
python init_data.py

# Avvia server
python main.py
```

✅ Backend avviato su: http://localhost:8000

### 3️⃣ Setup Frontend (3 minuti)

Apri un **nuovo terminale**:

```bash
cd frontend

# Installa dipendenze
npm install

# Avvia server
npm run dev
```

✅ Frontend avviato su: http://localhost:3000

---

## 🎯 Primo Accesso

### Login come Operatore

1. Apri http://localhost:3000
2. Inserisci nome: "Maria" (o qualsiasi nome)
3. Seleziona appartamento: "Appartamento 1"
4. Lascia data di oggi
5. Click "Inizia Turno"

➡️ Ora puoi:
- ✅ Completare la checklist
- 📦 Aggiornare l'inventario
- 📸 Caricare foto

### Login come Manager

1. Esci dall'account operatore
2. Inserisci nome: "Manager"
3. Seleziona qualsiasi appartamento
4. Click "Inizia Turno"

➡️ Ora puoi:
- 📊 Vedere la dashboard
- 📈 Visualizzare statistiche
- 📥 Esportare report

---

## 📱 Test da Smartphone

### Opzione A: Stesso WiFi
1. Trova indirizzo IP del tuo computer:
   ```bash
   # macOS/Linux
   ifconfig | grep "inet "
   # Windows
   ipconfig
   ```
2. Apri da smartphone: `http://TUO_IP:3000`

### Opzione B: Tunnel (ngrok)
```bash
# Installa ngrok
brew install ngrok  # macOS
# O scarica da ngrok.com

# Crea tunnel
ngrok http 3000

# Usa URL generato (es: https://abc123.ngrok.io)
```

---

## 🧪 Dati di Test Pre-caricati

Dopo aver eseguito `init_data.py`, avrai:

### Appartamenti (4)
- Appartamento 1 (Piano terra, 2 camere)
- Appartamento 2 (Primo piano, monolocale)
- Appartamento 3 (Secondo piano, 3 camere)
- Appartamento 4 (Attico, 2 camere con terrazzo)

### Utenti
- Manager (ruolo: manager)
- Tutti gli altri nomi vengono creati al primo login

### Categorie Inventario (5)
- Cucina
- Bagno
- Camera
- Consumabili
- Pulizia

### Articoli Inventario (20 per appartamento)
Esempi:
- Bicchieri (6 pz, min: 4)
- Asciugamani (4 pz, min: 2)
- Cialde caffè (20 pz, min: 10)
- Carta igienica (6 rotoli, min: 3)
- ecc.

### Template Checklist
Checklist standard con 9 task:
- Aspirare/lavare pavimenti ✓
- Pulire bagno completo ✓
- Cambiare biancheria letto ✓
- Pulire cucina e fornelli ✓
- Svuotare cestini ✓
- Rifornire consumabili ✓
- Controllo inventario (Sì/No) ✓
- Foto stato finale (Upload)
- Note aggiuntive (Testo)

---

## 🔍 Verifica Installazione

### Backend Health Check
```bash
curl http://localhost:8000/health
# Risposta attesa: {"status":"healthy"}
```

### API Documentation
Apri: http://localhost:8000/docs

### Frontend Build Test
```bash
cd frontend
npm run build
# Se non ci sono errori, tutto ok!
```

---

## ❓ Problemi Comuni

### "Connection refused" al database
```bash
# Verifica che PostgreSQL sia avviato
# macOS:
brew services start postgresql

# Linux:
sudo systemctl start postgresql

# Windows:
# Avvia servizio PostgreSQL dal Services Manager
```

### "Module not found" (Backend)
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### "Cannot find module" (Frontend)
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Upload foto non funziona
```bash
cd backend
mkdir uploads
chmod 777 uploads
```

### CORS errors
Verifica che in `backend/.env`:
```
CORS_ORIGINS=http://localhost:3000
```

---

## 🎉 Tutto Pronto!

Ora puoi:
1. ✅ Fare login come operatore
2. ✅ Completare checklist
3. ✅ Aggiornare inventario
4. ✅ Fare login come manager
5. ✅ Vedere dashboard
6. ✅ Esportare report

## 📚 Prossimi Passi

- Leggi [README.md](README.md) per documentazione completa
- Personalizza checklist in database
- Configura articoli inventario
- Setup deployment produzione

## 💡 Tips

- Usa Chrome DevTools Device Mode per simulare mobile
- Testa upload foto con immagini piccole (<1MB)
- Manager può vedere tutte le checklist e inventory
- Gli alert si generano automaticamente quando scorte < minimo

---

**Buon lavoro! 🚀**



