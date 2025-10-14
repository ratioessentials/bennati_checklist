# 🔧 Configurazione Apache (invece di Nginx)

## Se in Plesk vedi SOLO "Additional Apache directives"

Usa questa configurazione Apache:

```apache
# Abilita moduli proxy (potrebbero essere già attivi)
<IfModule mod_proxy.c>
    ProxyRequests Off
    ProxyPreserveHost On
    
    # Proxy per API
    ProxyPass /api http://localhost:8000/api
    ProxyPassReverse /api http://localhost:8000/api
    
    # Proxy per uploads
    ProxyPass /uploads http://localhost:8000/uploads
    ProxyPassReverse /uploads http://localhost:8000/uploads
    
    # Proxy per health
    ProxyPass /health http://localhost:8000/health
    ProxyPassReverse /health http://localhost:8000/health
    
    # Proxy per docs (API documentation)
    ProxyPass /docs http://localhost:8000/docs
    ProxyPassReverse /docs http://localhost:8000/docs
</IfModule>
```

## ⚠️ Problema Potenziale

Apache potrebbe **non** avere i moduli proxy attivi. Se dopo aver salvato vedi errori tipo:

- "Invalid command 'ProxyPass'"
- "mod_proxy not loaded"

Allora serve abilitare i moduli (richiede accesso SSH):

```bash
# Su Debian/Ubuntu
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2

# Su CentOS/RHEL
# I moduli sono solitamente già caricati
```

## ✅ Verifica Configurazione

Dopo aver salvato, testa:

```bash
curl https://eloquent-benz.95-110-229-242.plesk.page/api/health
```

Dovrebbe restituire: `{"status":"healthy"}`

---

## 🎯 CONSIGLIO: Usa Nginx invece

Apache funziona, ma Nginx è:
- ✅ Più veloce per proxy
- ✅ Meno memoria
- ✅ Standard su Plesk moderno

Per abilitare Nginx:
1. Apache & nginx Settings
2. Trova "nginx settings" o "Proxy mode"  
3. Abilita "Proxy mode"
4. Usa la configurazione Nginx (più semplice)

