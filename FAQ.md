# ❓ Domande Frequenti (FAQ)

## Generale

### Cos'è Bennati Checklist?
Un'applicazione web mobile-first per gestire le pulizie di appartamenti, con checklist dinamiche, gestione inventario e reportistica per manager.

### Chi può usarla?
- **Operatori**: Addetti alle pulizie che compilano checklist e aggiornano inventario
- **Manager**: Supervisori che monitorano attività, scorte e generano report

### Funziona offline?
Attualmente no. È necessaria connessione internet. Il supporto offline è pianificato per versioni future.

### È gratis?
Sì, il codice è open source con licenza MIT.

## Installazione

### Quali sono i requisiti di sistema?
- **Backend**: Python 3.9+, PostgreSQL 14+
- **Frontend**: Node.js 18+
- **Browser**: Chrome/Safari/Firefox ultimi 2 versioni

### Posso usare MySQL invece di PostgreSQL?
Sì, ma richiede modifiche al codice. PostgreSQL è raccomandato per compatibilità completa.

### Come aggiorno l'applicazione?
```bash
git pull origin main
cd backend && pip install -r requirements.txt --upgrade
cd ../frontend && npm install
```

## Utilizzo

### Come aggiungo un nuovo appartamento?
**Opzione 1 - Via API:**
```bash
curl -X POST http://localhost:8000/api/apartments/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Appartamento 5", "description": "Nuovo"}'
```

**Opzione 2 - Via Database:**
```sql
INSERT INTO apartments (name, description) 
VALUES ('Appartamento 5', 'Descrizione');
```

### Come creo una checklist personalizzata?
1. Accedi al database
2. Crea un nuovo `checklist_template`
3. Aggiungi `task_templates` associati
4. Al login, il template verrà usato automaticamente

### Come modifico gli articoli dell'inventario?
Modifica direttamente nel database o crea script Python:
```python
from database import SessionLocal
from models import InventoryItem

db = SessionLocal()
item = InventoryItem(
    apartment_id=1,
    category_id=1,
    name="Nuovo articolo",
    quantity=10,
    min_quantity=5,
    unit="pz"
)
db.add(item)
db.commit()
```

### Posso eliminare una checklist completata?
Sì, via API o database, ma **non è consigliato** per mantenere storico.

### Come cambio il ruolo di un utente?
```sql
UPDATE users SET role = 'manager' WHERE name = 'NomeUtente';
```

## Problemi Comuni

### "Connection refused" al database
**Soluzione:**
1. Verifica che PostgreSQL sia avviato
2. Controlla credenziali in `.env`
3. Testa connessione: `psql -d bennati_checklist -U postgres`

### Upload foto non funziona
**Possibili cause:**
1. Cartella `uploads/` non esiste → `mkdir backend/uploads`
2. Permessi insufficienti → `chmod 777 backend/uploads`
3. File troppo grande → Max 10MB
4. Formato non supportato → Solo immagini/video

### Frontend non si connette al backend
**Verifica:**
1. Backend è avviato su porta 8000
2. CORS configurato correttamente in `backend/.env`
3. Proxy funzionante in `vite.config.js`
4. Firewall non blocca porta 8000

### Alert non si generano automaticamente
**Controlla:**
1. `min_quantity` è impostato correttamente
2. Aggiornamento inventario salvato con successo
3. Check logs backend per errori

### Pagina bianca dopo login
**Debug:**
1. Apri Console browser (F12)
2. Controlla errori JavaScript
3. Verifica risposta API login
4. Controlla localStorage contiene dati utente

## Sicurezza

### È sicuro per la produzione?
**Richiede configurazioni aggiuntive:**
- [ ] HTTPS (certificato SSL)
- [ ] Secret key forte e unica
- [ ] Database password complessa
- [ ] CORS limitato a domini specifici
- [ ] Rate limiting
- [ ] Backup automatici

### Come cambio la secret key?
1. Genera nuova key: `python -c "import secrets; print(secrets.token_hex(32))"`
2. Aggiorna in `backend/.env`: `SECRET_KEY=nuova_key`
3. Riavvia backend
4. **Nota**: Tutti i token esistenti saranno invalidati

### I dati sono criptati?
- **In transito**: Solo se HTTPS è configurato
- **A riposo**: PostgreSQL supporta encryption at rest (da configurare)
- **Password**: App non usa password utente (solo nome)

## Performance

### Quanti utenti può supportare?
Setup base: **~50 utenti simultanei**  
Con ottimizzazioni: **~500 utenti**  
Per più utenti: Serve scaling orizzontale

### L'app è lenta, come ottimizzare?
**Backend:**
- Aggiungi indici database su colonne frequenti
- Usa connection pooling
- Cache con Redis

**Frontend:**
- Code splitting
- Image optimization
- Service Worker per cache

### Posso usare un database cloud?
Sì! Compatibile con:
- AWS RDS (PostgreSQL)
- Google Cloud SQL
- Azure Database
- Heroku Postgres

Solo modifica `DATABASE_URL` in `.env`.

## Personalizzazione

### Posso cambiare i colori?
Sì, modifica variabili CSS in `frontend/src/index.css`:
```css
:root {
  --primary: #TUO_COLORE;
  --secondary: #TUO_COLORE;
  /* etc */
}
```

### Posso aggiungere campi custom?
Sì, ma richiede:
1. Modifica `models.py` (backend)
2. Modifica `schemas.py` (backend)
3. Migrazione database (Alembic)
4. Update componenti frontend

### Supporta multilingua?
Non ancora. Pianificato per v1.1.0.  
Contributi benvenuti!

## Deployment

### Come faccio il deploy in produzione?

**Opzione 1 - VPS (Digital Ocean, Linode):**
1. Usa Docker Compose
2. Configura Nginx reverse proxy
3. Setup SSL con Let's Encrypt
4. Configura backup automatici

**Opzione 2 - Cloud Platforms:**
- **Backend**: Heroku, Railway, Render
- **Frontend**: Vercel, Netlify
- **Database**: AWS RDS, Heroku Postgres

**Opzione 3 - Self-hosted:**
Guida completa in [DEPLOYMENT.md] (da creare)

### Posso usare su dominio personalizzato?
Sì! Configura:
1. DNS record → IP server
2. Nginx virtual host
3. SSL certificate
4. Update CORS origins in `.env`

## Backup e Ripristino

### Come faccio backup del database?
```bash
# Backup
pg_dump bennati_checklist > backup_$(date +%Y%m%d).sql

# Restore
psql bennati_checklist < backup_20251013.sql
```

Automatizza con cron:
```bash
0 2 * * * pg_dump bennati_checklist > /backups/bennati_$(date +\%Y\%m\%d).sql
```

### Devo fare backup anche di uploads/?
Sì! Contiene foto/video caricati. Backup separato:
```bash
tar -czf uploads_backup.tar.gz backend/uploads/
```

## Integrations

### Posso integrare con altri sistemi?
Sì, l'API REST è completamente documentata su `/docs`.  
Esempi: sistemi contabilità, ERP, notifiche Slack/Teams.

### C'è un'app mobile nativa?
No, ma l'app web è ottimizzata per mobile (PWA-ready).

### Posso esportare dati in Excel?
Sì, export CSV disponibile. Apri in Excel o Google Sheets.

## Supporto

### Dove trovo aiuto?
1. Leggi questa FAQ
2. Controlla [README.md](README.md)
3. Cerca in GitHub Issues
4. Apri nuova Issue
5. Email: support@bennati-checklist.com

### Come segnalo un bug?
Apri Issue su GitHub con:
- Descrizione problema
- Passi per riprodurre
- Screenshot
- Versione browser/OS

### Posso richiedere nuove funzionalità?
Sì! Apri Issue con tag `enhancement`.

## Contribuire

### Come posso contribuire?
Vedi [CONTRIBUIRE.md](CONTRIBUIRE.md) per dettagli.

### Accettate donazioni?
Al momento no, ma contributi code sono sempre benvenuti!

---

**Non trovi risposta?** Apri una [Discussion](https://github.com/bennati/issues) su GitHub!



