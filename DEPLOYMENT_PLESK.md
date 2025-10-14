# 🚀 Guida Deployment su Plesk

## 📋 Prerequisiti

- Accesso SSH al server Plesk
- Node.js 18+ installato sul server
- Git configurato
- Database PostgreSQL disponibile

## 🔧 Configurazione Plesk

### 1. Impostazioni Git

In Plesk, nella sezione **Git**:
- Repository: `https://github.com/tuousername/bennati_checklist.git`
- Branch: `main`
- Deploy path: `/var/www/vhosts/tuodominio.com/httpdocs`

### 2. Document Root

**IMPORTANTE**: Imposta il Document Root su:
```
/var/www/vhosts/tuodominio.com/httpdocs/frontend/dist
```

Oppure se Plesk usa percorsi relativi:
```
frontend/dist
```

### 3. Script di Deploy

Aggiungi questo script in Plesk > Git > "Additional deploy actions":

```bash
#!/bin/bash
set -e

echo "🔧 Installazione dipendenze backend..."
cd backend
pip3 install -r requirements.txt --user

echo "🎨 Build frontend..."
cd ../frontend
npm install
npm run build

echo "✅ Deploy completato!"
echo "📁 Frontend disponibile in: frontend/dist/"
```

## 🗄️ Configurazione Database

### 1. Crea Database PostgreSQL

In Plesk > Databases:
- Nome database: `bennati_checklist`
- Utente: `bennati`
- Password: (genera password sicura)

### 2. Configura Backend

Crea file `backend/.env` via SSH o File Manager:

```bash
DATABASE_URL=postgresql://bennati:TUA_PASSWORD@localhost:5432/bennati_checklist
SECRET_KEY=genera-una-chiave-sicura-qui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
UPLOAD_DIR=/var/www/vhosts/tuodominio.com/uploads
CORS_ORIGINS=https://tuodominio.com
```

**Genera SECRET_KEY sicura:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Inizializza Database

Via SSH:
```bash
cd /var/www/vhosts/tuodominio.com/httpdocs/backend
python3 init_data.py
```

## 🔌 Configurazione Backend API

### Opzione A: Passenger (Python)

Se Plesk supporta Passenger per Python:

1. In Plesk > Apache & Nginx Settings > Additional directives:

```apache
PassengerEnabled on
PassengerAppType wsgi
PassengerStartupFile backend/passenger_wsgi.py
```

2. Crea `backend/passenger_wsgi.py`:

```python
import sys
import os

# Aggiungi path
sys.path.insert(0, os.path.dirname(__file__))

# Import app FastAPI
from main import app

# WSGI application
application = app
```

### Opzione B: Systemd Service (CONSIGLIATO)

1. Crea `/etc/systemd/system/bennati-backend.service`:

```ini
[Unit]
Description=Bennati Checklist Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/vhosts/tuodominio.com/httpdocs/backend
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Avvia servizio:
```bash
sudo systemctl daemon-reload
sudo systemctl enable bennati-backend
sudo systemctl start bennati-backend
```

### Opzione C: Proxy Inverso Nginx

Configura Nginx in Plesk per fare proxy al backend:

In Plesk > Apache & Nginx Settings > Additional nginx directives:

```nginx
location /api {
    proxy_pass http://localhost:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location /uploads {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location /docs {
    proxy_pass http://localhost:8000;
}

location /health {
    proxy_pass http://localhost:8000;
}
```

## 📁 Struttura File dopo Deploy

```
/var/www/vhosts/tuodominio.com/
├── httpdocs/                    # Document root punta qui
│   ├── backend/
│   │   ├── .env                 # Configurazione (NON committare!)
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── ...
│   ├── frontend/
│   │   ├── dist/                # ← Document Root finale
│   │   │   ├── index.html
│   │   │   ├── assets/
│   │   │   └── ...
│   │   ├── src/
│   │   └── package.json
│   └── ...
└── uploads/                     # Fuori da httpdocs per sicurezza
```

## ✅ Verifica Deployment

### 1. Test Frontend
```bash
curl https://tuodominio.com
# Dovrebbe restituire l'HTML dell'app React
```

### 2. Test Backend
```bash
curl https://tuodominio.com/api/health
# Dovrebbe restituire: {"status":"healthy"}
```

### 3. Test Database
```bash
curl https://tuodominio.com/api/apartments
# Dovrebbe restituire lista appartamenti
```

## 🔄 Aggiornamenti

Per aggiornare l'applicazione:

1. In Plesk > Git > click "Pull"
2. Gli script di deploy si eseguiranno automaticamente
3. Se necessario, riavvia backend:
```bash
sudo systemctl restart bennati-backend
```

## 🛠️ Troubleshooting

### Frontend non si vede
- Verifica Document Root: deve puntare a `frontend/dist`
- Controlla che `npm run build` sia stato eseguito
- Verifica permessi file (644 per file, 755 per directory)

### Backend non risponde
- Verifica servizio: `sudo systemctl status bennati-backend`
- Controlla logs: `journalctl -u bennati-backend -f`
- Verifica porta 8000: `netstat -tlnp | grep 8000`

### Database connection error
- Verifica credenziali in `backend/.env`
- Controlla che PostgreSQL sia avviato
- Verifica permessi utente database

### CORS errors
- Verifica `CORS_ORIGINS` in `backend/.env`
- Deve includere il dominio: `https://tuodominio.com`

### Upload foto non funziona
- Verifica cartella uploads esista e sia scrivibile
- Controlla permessi: `chmod 777 /var/www/vhosts/tuodominio.com/uploads`
- Verifica `UPLOAD_DIR` in `.env`

## 🔒 Sicurezza

### 1. File Permissions
```bash
cd /var/www/vhosts/tuodominio.com/httpdocs
chmod 600 backend/.env
chmod 755 backend
chmod 755 frontend/dist
chmod 777 ../uploads
```

### 2. .gitignore
Assicurati che `.gitignore` contenga:
```
.env
uploads/
*.pyc
__pycache__/
node_modules/
frontend/dist/
```

### 3. SSL/HTTPS
In Plesk > SSL/TLS Certificates:
- Attiva "Let's Encrypt"
- Forza HTTPS redirect

### 4. Firewall
Apri solo porte necessarie:
- 80 (HTTP - redirect a HTTPS)
- 443 (HTTPS)
- 8000 (Backend - solo localhost se usi proxy)

## 📊 Monitoraggio

### Logs Backend
```bash
# Systemd service
journalctl -u bennati-backend -f

# O se usi file log
tail -f /var/log/bennati-backend.log
```

### Logs Nginx/Apache
```bash
tail -f /var/www/vhosts/tuodominio.com/logs/error_log
tail -f /var/www/vhosts/tuodominio.com/logs/access_log
```

## 💾 Backup

### Database
```bash
# Backup
pg_dump -U bennati bennati_checklist > backup_$(date +%Y%m%d).sql

# Restore
psql -U bennati bennati_checklist < backup_20251014.sql
```

### File Upload
```bash
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz /var/www/vhosts/tuodominio.com/uploads/
```

## 🎯 Checklist Pre-Deploy

- [ ] Database PostgreSQL creato
- [ ] File `backend/.env` configurato
- [ ] SECRET_KEY generata (sicura!)
- [ ] CORS_ORIGINS corretto
- [ ] Document Root impostato su `frontend/dist`
- [ ] Script deploy configurato
- [ ] Nginx proxy per `/api` configurato
- [ ] Servizio backend attivo
- [ ] SSL/HTTPS attivo
- [ ] Firewall configurato
- [ ] Backup automatici configurati

---

**Buon deployment! 🚀**

