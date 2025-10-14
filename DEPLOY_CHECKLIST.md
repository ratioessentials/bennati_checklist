# ⚠️ CHECKLIST DEPLOY SU PLESK

## 🚨 ATTENZIONE - BREAKING CHANGES

Le ultime modifiche hanno cambiato lo **schema del database**:
- Aggiunto campo `username` alla tabella `users`
- Aggiunto campo `password_hash` alla tabella `users`
- **Il vecchio database NON è compatibile!**

### ❗ Prima del Deploy

**SE HAI GIÀ UN DATABASE SU PLESK:** Devi resettarlo!

```bash
# Connettiti via SSH a Plesk e esegui:
cd /var/www/vhosts/tuodominio.plesk.page/httpdocs/backend
python3 << 'EOF'
from database import engine, Base
Base.metadata.drop_all(bind=engine)  # ATTENZIONE: Cancella tutto!
Base.metadata.create_all(bind=engine)
EOF

# Poi reinizializza i dati:
python3 init_data.py
```

## ✅ Checklist Pre-Deploy

### 1. File da Committare

- [ ] `.plesk.yml` - ✅ Già tracciato
- [ ] `backend/.env.example` - ✅ Esiste
- [ ] `backend/passenger_wsgi.py` - ✅ Creato
- [ ] `DEPLOY_QUICK.md` - ✅ Già tracciato
- [ ] Modifiche al codice (models, auth, schemas, login)

### 2. File da NON Committare (verificati)

- [x] `.env` - ✅ In .gitignore
- [x] `node_modules/` - ✅ In .gitignore
- [x] `frontend/dist/` - ✅ In .gitignore
- [x] `uploads/` - ✅ In .gitignore
- [x] `__pycache__/` - ✅ In .gitignore

### 3. Configurazione Plesk

- [ ] **Document Root** impostato su: `frontend/dist`
- [ ] **Database PostgreSQL** creato
- [ ] File `backend/.env` creato con credenziali corrette
- [ ] **Proxy Nginx** configurato per `/api`
- [ ] Backend in esecuzione (porta 8000)

## 📝 Comandi Deploy

### Passo 1: Commit e Push

```bash
git add -A
git commit -m "Sistema login con username/password + pulizia documentazione"
git push origin main
```

### Passo 2: Deploy su Plesk

In Plesk > Git > **Deploy**

Lo script `.plesk.yml` farà automaticamente:
- ✅ Installa dipendenze Python
- ✅ Installa dipendenze Node
- ✅ Build frontend
- ✅ Crea cartella uploads

### Passo 3: Configurazione Backend (SSH)

```bash
# Connettiti via SSH
ssh utente@eloquent-benz.95-110-229-242.plesk.page

# Vai alla directory
cd /var/www/vhosts/eloquent-benz.95-110-229-242.plesk.page/httpdocs

# Crea file .env
cd backend
cp .env.example .env

# MODIFICA .env con le tue credenziali!
nano .env
```

Contenuto `.env`:
```bash
DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/DBNAME
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
CORS_ORIGINS=https://eloquent-benz.95-110-229-242.plesk.page
UPLOAD_DIR=/var/www/vhosts/eloquent-benz.95-110-229-242.plesk.page/uploads
```

### Passo 4: Reset Database (IMPORTANTE!)

```bash
cd backend
python3 init_data.py
```

Output atteso:
```
✅ Appartamenti creati
✅ 4 utenti operatori creati (sofia, giulia, martina, chiara) - password: Prova123!
✅ Categorie inventario create
✅ Articoli inventario creati
✅ Template checklist creato

🔑 Credenziali login:
   Username: sofia, giulia, martina o chiara
   Password: Prova123!
```

### Passo 5: Avvia Backend

Opzione A - Con systemd (CONSIGLIATO):
```bash
sudo nano /etc/systemd/system/bennati-backend.service
```

Contenuto:
```ini
[Unit]
Description=Bennati Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/vhosts/eloquent-benz.95-110-229-242.plesk.page/httpdocs/backend
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Poi:
```bash
sudo systemctl daemon-reload
sudo systemctl enable bennati-backend
sudo systemctl start bennati-backend
sudo systemctl status bennati-backend
```

Opzione B - Manuale (per test):
```bash
cd backend
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 &
```

### Passo 6: Configura Nginx Proxy

In Plesk > Apache & nginx Settings > Additional nginx directives:

```nginx
location /api {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location /uploads {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
}

location /health {
    proxy_pass http://localhost:8000;
}

location /docs {
    proxy_pass http://localhost:8000;
}
```

Salva e riavvia Nginx.

## 🧪 Test Deploy

### 1. Test Frontend
```bash
curl https://eloquent-benz.95-110-229-242.plesk.page/
# Deve restituire HTML dell'app React
```

### 2. Test Backend
```bash
curl https://eloquent-benz.95-110-229-242.plesk.page/api/health
# Deve restituire: {"status":"healthy"}
```

### 3. Test Login
Vai su: https://eloquent-benz.95-110-229-242.plesk.page

- Username: `sofia`
- Password: `Prova123!`
- Appartamento: Monolocale
- Data: oggi

Se tutto funziona: ✅ Deploy completato!

## 🐛 Troubleshooting

### Frontend mostra pagina Plesk default
- ❌ Document Root non impostato correttamente
- ✅ Imposta su: `frontend/dist`

### "Cannot GET /api/..."
- ❌ Backend non in esecuzione
- ✅ Avvia backend: `systemctl start bennati-backend`
- ✅ Controlla: `systemctl status bennati-backend`

### "Username o password non corretti"
- ❌ Database non inizializzato
- ✅ Esegui: `python3 init_data.py`

### CORS errors
- ❌ CORS_ORIGINS non include il dominio
- ✅ Verifica `backend/.env`: `CORS_ORIGINS=https://eloquent-benz.95-110-229-242.plesk.page`

### 500 Internal Server Error
- ❌ Errore nel backend
- ✅ Controlla logs: `journalctl -u bennati-backend -f`

## 📊 Nuovo Sistema di Login

### ⚠️ Cambiamenti Importanti

**VECCHIO Sistema:**
- ❌ Nome libero senza password
- ❌ Creava utenti al volo

**NUOVO Sistema:**
- ✅ Login con username/password
- ✅ 4 account predefiniti
- ✅ Password hashate con bcrypt
- ✅ Sicurezza migliorata

### 👥 Account Disponibili

| Username | Password | Nome |
|----------|----------|------|
| sofia | Prova123! | Sofia |
| giulia | Prova123! | Giulia |
| martina | Prova123! | Martina |
| chiara | Prova123! | Chiara |

---

**Ready to deploy! 🚀**

