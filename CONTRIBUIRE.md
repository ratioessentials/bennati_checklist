# 🤝 Come Contribuire

Grazie per l'interesse nel contribuire a Bennati Checklist!

## 🐛 Segnalare Bug

1. Controlla che il bug non sia già stato segnalato nelle Issues
2. Crea una nuova Issue con:
   - Titolo descrittivo
   - Passi per riprodurre
   - Comportamento atteso vs effettivo
   - Screenshot se applicabile
   - Versione browser/OS

## 💡 Proporre Nuove Funzionalità

1. Apri una Issue con tag `enhancement`
2. Descrivi:
   - Il problema che risolverebbe
   - La soluzione proposta
   - Alternative considerate
   - Mockup/wireframe se disponibili

## 🔧 Pull Request

### Setup Ambiente Sviluppo

```bash
# Fork il repository
git clone https://github.com/TUO_USERNAME/bennati_checklist.git
cd bennati_checklist

# Crea branch per la tua feature
git checkout -b feature/nome-feature

# Segui setup in README.md
./setup.sh
```

### Convenzioni Codice

**Python (Backend):**
- Segui PEP 8
- Type hints dove possibile
- Docstrings per funzioni pubbliche
- Max line length: 100 caratteri

```python
def update_inventory_item(
    item_id: int, 
    quantity: int, 
    db: Session
) -> InventoryItem:
    """
    Aggiorna la quantità di un articolo inventario.
    
    Args:
        item_id: ID articolo da aggiornare
        quantity: Nuova quantità
        db: Sessione database
        
    Returns:
        Articolo aggiornato
    """
    # ... implementazione
```

**JavaScript (Frontend):**
- ESLint configurato nel progetto
- Componenti funzionali + Hooks
- Props destructuring
- Commenti JSDoc per funzioni complesse

```javascript
/**
 * Aggiorna una task della checklist
 * @param {number} taskId - ID della task
 * @param {Object} updates - Modifiche da applicare
 */
const handleTaskUpdate = async (taskId, updates) => {
  // ... implementazione
};
```

### Commit Messages

Usa [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: aggiunta funzionalità stampa checklist
fix: corretto bug upload foto su iOS
docs: aggiornata documentazione API
style: formattazione codice backend
refactor: ristrutturato componente InventoryPage
test: aggiunti test per inventario
chore: aggiornate dipendenze npm
```

### Testing

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

Assicurati che tutti i test passino prima di fare PR.

### Processo Pull Request

1. **Aggiorna il tuo fork**
   ```bash
   git remote add upstream https://github.com/bennati/bennati_checklist.git
   git fetch upstream
   git merge upstream/main
   ```

2. **Crea branch feature**
   ```bash
   git checkout -b feature/nome-feature
   ```

3. **Implementa modifiche**
   - Scrivi codice
   - Aggiungi test
   - Aggiorna documentazione

4. **Commit e push**
   ```bash
   git add .
   git commit -m "feat: descrizione feature"
   git push origin feature/nome-feature
   ```

5. **Apri Pull Request**
   - Vai su GitHub
   - Click "New Pull Request"
   - Descrivi le modifiche
   - Riferisci Issue correlate

6. **Code Review**
   - Rispondi ai commenti
   - Applica modifiche richieste
   - Push aggiornamenti

### Checklist PR

- [ ] Codice segue convenzioni del progetto
- [ ] Test aggiunti/aggiornati e passano
- [ ] Documentazione aggiornata
- [ ] No warning linter
- [ ] Commit messages seguono convenzioni
- [ ] Branch aggiornato con main
- [ ] Testato su mobile (se frontend)

## 📁 Struttura Progetto

```
bennati_checklist/
├── backend/          # FastAPI backend
│   ├── routers/     # API endpoints
│   ├── models.py    # Database models
│   └── schemas.py   # Pydantic schemas
├── frontend/         # React frontend
│   └── src/
│       ├── pages/   # Page components
│       ├── components/ # Reusable components
│       └── services/   # API client
└── docs/            # Documentazione
```

## 🎯 Aree Prioritarie

Contributi particolarmente benvenuti su:

1. **Testing**
   - Unit test backend
   - Component test frontend
   - E2E test

2. **Accessibilità**
   - ARIA labels
   - Keyboard navigation
   - Screen reader support

3. **Performance**
   - Ottimizzazioni query database
   - Code splitting frontend
   - Image optimization

4. **Internazionalizzazione**
   - Setup i18n
   - Traduzione italiano/inglese

5. **Mobile UX**
   - PWA support
   - Offline mode
   - Push notifications

## ❓ Domande

- Apri una Discussion su GitHub
- Email: dev@bennati-checklist.com

## 📜 Codice di Condotta

Sii rispettoso, collaborativo e costruttivo. Tutti i contributi sono benvenuti indipendentemente da:
- Livello di esperienza
- Background
- Identità personale

Comportamenti inappropriati non saranno tollerati.

## 🙏 Grazie!

Ogni contributo, grande o piccolo, è apprezzato!

---

**Happy Coding! 🚀**



