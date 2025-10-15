# ⚡ Deploy Rapido su Plesk

## 🎯 Passi Essenziali

### 1. Configura Document Root in Plesk
```
frontend/dist
```
**IMPORTANTE**: Il Document Root deve puntare a `frontend/dist`, non alla root!

### 2. Crea Database PostgreSQL
In Plesk > Databases:
- Nome: `bennati_checklist`
- Utente: `bennati`
- Password: (salvala!)

### 3. Configura Backend
Crea file `backend/.env` via SSH o File Manager:

```bash
DATABASE_URL=postgresql://bennati:TUA_PASSWORD@localhost:5432/bennati_checklist
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
UPLOAD_DIR=/var/www/vhosts/TUODOMINIO/uploads
CORS_ORIGINS=https://TUODOMINIO.com
```

### 4. Build Frontend
```bash
cd frontend
npm install
npm run build
```

### 5. Inizializza Database
```bash
cd backend
pip3 install -r requirements.txt --user
python3 init_data.py
```

### 6. Avvia Backend
```bash
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 &
```

### 7. Configura Nginx Proxy
In Plesk > Apache & Nginx Settings > Additional nginx directives:

```nginx
location /api {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
}

location /uploads {
    proxy_pass http://localhost:8000;
}
```

## ✅ Test
- Frontend: https://TUODOMINIO.com
- Backend: https://TUODOMINIO.com/api/health

---

📚 **Guida completa**: vedi `DEPLOYMENT_PLESK.md`

