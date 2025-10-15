# 🎯 Setup Plesk SEMPLIFICATO

## Step 1: Configurazione PRIMA del Deploy

### 1.1 Crea Database PostgreSQL in Plesk

1. Vai su **Database** in Plesk
2. Click **Add Database**
3. Compila:
   - Nome database: `bennati_checklist`
   - Utente: `bennati`
   - Password: (genera una sicura e salvala!)

### 1.2 Configura Document Root

1. Vai su **Hosting Settings**
2. Trova **Document root**
3. Cambia da `httpdocs` a: `httpdocs/frontend/dist`
4. **Salva**

### 1.3 Configura Proxy Web Server (UNA VOLTA SOLA)

**Cosa fa:** Il web server inoltra le chiamate API al backend che gira sulla stessa macchina (localhost:8000)

**Perché localhost?** Backend e web server girano SULLO STESSO server. "localhost" = "questa macchina".

**Flusso:**
```
Utente → tuodominio.com/api/health
        ↓ (Web server riceve)
        ↓ (Inoltra internamente)
Backend su localhost:8000 → Risponde
        ↓ (Restituisce)
Utente ← Riceve risposta
```

---

### 🔍 PRIMA: Verifica quale web server hai

1. Vai su **Apache & nginx Settings** (nel menu del tuo dominio)
2. Controlla se vedi:
   - ✅ **"Additional nginx directives"** → Hai Nginx → Usa Opzione A
   - ❌ Solo **"Additional Apache directives"** → Solo Apache → Usa Opzione B

Se non vedi "nginx directives":
3. Cerca **"Proxy mode"** o **"nginx settings"** nella stessa pagina
4. Attiva **"Proxy mode"** o **"Smart static files processing"**
5. Salva → Ora dovresti vedere "Additional nginx directives"

---

### ✅ OPZIONE A: Nginx (CONSIGLIATO - più veloce)

**Se vedi "Additional nginx directives":**

1. Nel campo **Additional nginx directives**, incolla questo:

```nginx
location /api {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location /uploads {
    proxy_pass http://localhost:8000;
}

location /health {
    proxy_pass http://localhost:8000;
}
```

2. **Salva** (click su "OK" o "Apply")

**Come verificare:**
- Se vedi errori tipo "Invalid command 'location'" → Hai sbagliato campo! 
- Se salva senza errori → ✅ Perfetto!

---

### ⚙️ OPZIONE B: Solo Apache

**Se NON vedi "nginx directives" e hai solo Apache:**

1. Nel campo **Additional Apache directives**, incolla questo:

```apache
<IfModule mod_proxy.c>
    ProxyRequests Off
    ProxyPreserveHost On
    
    ProxyPass /api http://localhost:8000/api
    ProxyPassReverse /api http://localhost:8000/api
    
    ProxyPass /uploads http://localhost:8000/uploads
    ProxyPassReverse /uploads http://localhost:8000/uploads
    
    ProxyPass /health http://localhost:8000/health
    ProxyPassReverse /health http://localhost:8000/health
    
    ProxyPass /docs http://localhost:8000/docs
    ProxyPassReverse /docs http://localhost:8000/docs
</IfModule>
```

2. **Salva**

**Se vedi errore "Invalid command ProxyPass":**
- Apache non ha i moduli proxy attivi
- Serve accesso SSH per abilitarli
- Oppure chiedi al supporto Plesk di abilitare mod_proxy

**Meglio abilitare Nginx** se possibile (Opzione A)!

---

## Step 2: Primo Deploy

### 2.1 Push su Git

```bash
git add -A
git commit -m "Setup iniziale con login"
git push origin main
```

### 2.2 Deploy in Plesk

1. Vai su **Git** in Plesk
2. Click **Deploy**
3. Aspetta che finisca (1-2 minuti)

---

## Step 3: Configurazione .env (UNA VOLTA SOLA)

### Opzione A: Via File Manager Plesk (PIÙ SEMPLICE)

1. Vai su **File Manager** in Plesk
2. Naviga in `httpdocs/backend/`
3. Trovi il file `.env` (creato automaticamente)
4. Click **Edit**
5. Modifica queste righe:

```bash
DATABASE_URL=postgresql://bennati:LA_TUA_PASSWORD@localhost:5432/bennati_checklist
SECRET_KEY=genera-una-chiave-sicura-qui
CORS_ORIGINS=https://eloquent-benz.95-110-229-242.plesk.page
```

Per generare SECRET_KEY:
- Apri terminal
- Esegui: `python3 -c "import secrets; print(secrets.token_hex(32))"`
- Copia il risultato

6. **Salva**

### Opzione B: Via SSH (se preferisci)

```bash
cd httpdocs/backend
nano .env
# Modifica e salva
```

---

## Step 4: Riavvia (dopo aver configurato .env)

### Opzione A: Re-Deploy da Plesk (SEMPLICISSIMO)

1. Vai su **Git** in Plesk
2. Click **Deploy** di nuovo
3. Fatto! ✅

Lo script automatico:
- ✅ Reinstalla dipendenze
- ✅ Rebuilda frontend
- ✅ Inizializza database
- ✅ Avvia backend

### Opzione B: Via SSH

```bash
cd httpdocs
pkill -f uvicorn
cd backend
python3 init_data.py
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 &
```

---

## ✅ Test Finale

1. Vai su: https://eloquent-benz.95-110-229-242.plesk.page
2. Dovresti vedere la pagina di login
3. Prova a loggarti:
   - Username: `sofia`
   - Password: `Prova123!`
   - Appartamento: Monolocale
   - Click "Inizia Turno"

Se funziona: **🎉 TUTTO OK!**

---

## 🔄 Aggiornamenti Futuri

Ogni volta che fai modifiche al codice:

```bash
git add -A
git commit -m "Descrizione modifiche"
git push origin main
```

Poi in Plesk: **Git → Deploy**

Lo script `.plesk.yml` farà tutto automaticamente! 🚀

---

## 🐛 Troubleshooting

### "Pagina bianca" o "Pagina Plesk default"
- ❌ Document Root non impostato
- ✅ Vai su Hosting Settings → Document root: `httpdocs/frontend/dist`

### "Cannot GET /api/health"
- ❌ Backend non avviato
- ✅ Re-deploy da Plesk (Git → Deploy)
- ✅ Controlla log: `backend.log`

### "Username o password non corretti"
- ❌ Database non inizializzato
- ✅ Verifica `.env` sia configurato correttamente
- ✅ Re-deploy da Plesk

### "Database connection error"
- ❌ Credenziali database sbagliate in `.env`
- ✅ Verifica password database in Plesk → Databases
- ✅ Aggiorna `DATABASE_URL` in `.env`

---

## 📋 Configurazioni da Fare UNA VOLTA SOLA

- [x] Crea database PostgreSQL
- [x] Imposta Document Root su `httpdocs/frontend/dist`
- [x] Configura Nginx proxy per `/api`
- [x] Configura `.env` con credenziali database
- [x] Primo deploy

## 🔁 Operazioni AUTOMATICHE ad Ogni Deploy

- ✅ Installa dipendenze Python
- ✅ Installa dipendenze Node
- ✅ Build frontend
- ✅ Inizializza database
- ✅ Riavvia backend

---

**Fatto! Molto più semplice! 🎯**

