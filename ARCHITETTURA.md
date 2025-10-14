# 🏗️ Architettura Tecnica - Bennati Checklist

Documentazione tecnica dettagliata dell'architettura del sistema.

## 📊 Diagramma Architettura

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  LoginPage   │  │ ChecklistPage│  │ InventoryPage│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────────────────────────────────────────┐     │
│  │         ManagerDashboard                          │     │
│  └──────────────────────────────────────────────────┘     │
│                          ↕                                  │
│  ┌──────────────────────────────────────────────────┐     │
│  │         API Client (Axios)                        │     │
│  └──────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                          ↕ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │  Users   │ │Apartments│ │Checklists│ │Inventory │     │
│  │  Router  │ │  Router  │ │  Router  │ │  Router  │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
│  ┌──────────────────────────────────────────────────┐     │
│  │         Reports Router                            │     │
│  └──────────────────────────────────────────────────┘     │
│                          ↕                                  │
│  ┌──────────────────────────────────────────────────┐     │
│  │         SQLAlchemy ORM                            │     │
│  └──────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                          ↕ SQL
┌─────────────────────────────────────────────────────────────┐
│                  DATABASE (PostgreSQL)                      │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐            │
│  │Users │ │Apts  │ │Checks│ │Tasks │ │Inv   │            │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘            │
└─────────────────────────────────────────────────────────────┘
```

## 🗂️ Database Schema

### Entità e Relazioni

```sql
-- Users (Operatori e Manager)
users
├── id (PK)
├── name
├── role (operatore/manager)
└── created_at

-- Apartments
apartments
├── id (PK)
├── name
├── description
└── created_at

-- Checklist Templates
checklist_templates
├── id (PK)
├── apartment_id (FK, nullable)
├── name
├── description
└── created_at

-- Task Templates
task_templates
├── id (PK)
├── template_id (FK)
├── title
├── description
├── task_type (checkbox/text/yes_no/photo)
├── order_index
└── required

-- Checklists (Sessioni)
checklists
├── id (PK)
├── user_id (FK)
├── apartment_id (FK)
├── date
├── completed
├── completed_at
└── notes

-- Task Responses
task_responses
├── id (PK)
├── checklist_id (FK)
├── task_template_id (FK)
├── completed
├── text_response
├── yes_no_response
├── photo_paths (JSON)
├── created_at
└── updated_at

-- Inventory Categories
inventory_categories
├── id (PK)
├── name
├── description
└── is_consumable

-- Inventory Items
inventory_items
├── id (PK)
├── apartment_id (FK)
├── category_id (FK)
├── name
├── quantity
├── min_quantity
├── unit
├── last_updated
└── last_updated_by (FK)

-- Inventory History
inventory_history
├── id (PK)
├── item_id (FK)
├── user_id (FK)
├── old_quantity
├── new_quantity
├── change_reason
└── created_at

-- Alerts
alerts
├── id (PK)
├── apartment_id (FK)
├── inventory_item_id (FK, nullable)
├── alert_type
├── message
├── severity
├── resolved
├── created_at
└── resolved_at
```

### Relazioni Principali

- **1:N** User → Checklist (un utente può avere molte checklist)
- **1:N** Apartment → Checklist (un appartamento ha molte checklist)
- **1:N** Apartment → InventoryItem (un appartamento ha molti articoli)
- **1:N** Checklist → TaskResponse (una checklist ha molte risposte)
- **1:N** InventoryItem → InventoryHistory (un articolo ha molti record storici)
- **1:N** InventoryCategory → InventoryItem (una categoria ha molti articoli)

## 🔐 Autenticazione e Autorizzazione

### Flow di Login

```
1. Utente inserisce nome + appartamento + data
   ↓
2. Backend crea/recupera User
   ↓
3. Backend crea nuova Checklist
   ↓
4. Backend genera JWT token
   ↓
5. Frontend salva token + dati in localStorage
   ↓
6. Tutte le richieste successive includono token nell'header
```

### JWT Token Structure

```json
{
  "sub": "user_id",
  "role": "operatore|manager",
  "exp": "timestamp"
}
```

### Ruoli e Permessi

| Risorsa | Operatore | Manager |
|---------|-----------|---------|
| Login | ✅ | ✅ |
| Checklist (proprie) | ✅ R/W | ✅ R |
| Checklist (tutte) | ❌ | ✅ R |
| Inventario (proprio apt) | ✅ R/W | ✅ R/W |
| Inventario (tutti apt) | ❌ | ✅ R/W |
| Dashboard | ❌ | ✅ R |
| Export Report | ❌ | ✅ R |

## 📡 API Design

### REST Principles

- **Resource-based URLs**: `/api/checklists/{id}`
- **HTTP Methods**: GET, POST, PUT, DELETE
- **Status Codes**: 200, 201, 400, 404, 500
- **JSON Response**: Consistente con schemi Pydantic

### Endpoints Pattern

```
/api/
├── users/
│   ├── POST /login
│   ├── GET /
│   └── GET /{id}
├── apartments/
│   ├── GET /
│   ├── POST /
│   ├── GET /{id}
│   ├── PUT /{id}
│   └── DELETE /{id}
├── checklists/
│   ├── GET /
│   ├── POST /
│   ├── GET /{id}
│   ├── PUT /{id}
│   ├── GET /{id}/tasks
│   ├── PUT /tasks/{id}
│   ├── POST /tasks/{id}/upload
│   └── templates/
│       ├── GET /
│       ├── POST /
│       └── GET /{id}
├── inventory/
│   ├── categories/
│   │   ├── GET /
│   │   └── POST /
│   ├── items/
│   │   ├── GET /
│   │   ├── POST /
│   │   ├── GET /{id}
│   │   ├── PUT /{id}
│   │   ├── DELETE /{id}
│   │   └── GET /{id}/history
│   └── alerts/
│       ├── GET /
│       ├── POST /
│       └── PUT /{id}/resolve
└── reports/
    ├── GET /dashboard
    ├── GET /apartment/{id}/inventory
    ├── GET /stats/apartment/{id}
    ├── GET /export/inventory/pdf
    ├── GET /export/inventory/csv
    └── GET /export/checklists/csv
```

### Request/Response Examples

**Login Request:**
```json
POST /api/users/login
{
  "name": "Maria",
  "apartment_id": 1,
  "date": "2025-10-13T10:00:00Z"
}
```

**Login Response:**
```json
{
  "user": {
    "id": 1,
    "name": "Maria",
    "role": "operatore",
    "created_at": "2025-10-13T10:00:00Z"
  },
  "apartment": {
    "id": 1,
    "name": "Appartamento 1",
    "description": "Piano terra, 2 camere"
  },
  "checklist": {
    "id": 42,
    "user_id": 1,
    "apartment_id": 1,
    "date": "2025-10-13T10:00:00Z",
    "completed": false,
    "task_responses": [...]
  },
  "access_token": "eyJhbGc..."
}
```

## 🎨 Frontend Architecture

### Component Hierarchy

```
App
├── AppProvider (Context)
├── Router
│   ├── LoginPage
│   └── Layout
│       ├── Header
│       ├── Navigation
│       ├── Outlet
│       │   ├── ChecklistPage
│       │   │   └── TaskItem (x9)
│       │   ├── InventoryPage
│       │   │   └── InventoryItem (x20)
│       │   └── ManagerDashboard
│       │       ├── StatsCards
│       │       ├── AlertsList
│       │       ├── ApartmentCards (x4)
│       │       └── RestockTable
│       └── Footer
└── ToastContainer
```

### State Management

**Global State (Context):**
- `user`: Utente corrente
- `apartment`: Appartamento selezionato
- `checklist`: Checklist attiva
- `loginUser()`: Login function
- `logout()`: Logout function
- `updateChecklist()`: Update checklist

**Local State (useState):**
- Ogni page/component gestisce il proprio stato locale
- Dati caricati via API calls
- Form inputs
- UI states (loading, errors)

### Data Flow

```
User Action
   ↓
Component Event Handler
   ↓
API Call (services/api.js)
   ↓
Backend Processing
   ↓
Database Update
   ↓
API Response
   ↓
Component State Update
   ↓
UI Re-render
```

## 📱 Mobile-First Strategy

### Breakpoints

```css
/* Mobile (default) */
@media (max-width: 768px) { ... }

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) { ... }

/* Desktop */
@media (min-width: 1025px) { ... }
```

### Touch Optimizations

- **Minimum touch target**: 44x44px (Apple HIG)
- **Font size**: ≥16px (evita zoom automatico iOS)
- **Spacing**: Generoso tra elementi cliccabili
- **Sticky elements**: Header e navigation fissi
- **Bottom actions**: Azioni principali in basso (pollice-friendly)

### Performance

- **Code splitting**: Route-based
- **Lazy loading**: Immagini e componenti pesanti
- **Caching**: API responses con React Query (potenziale upgrade)
- **Service Worker**: Per offline support (futuro)

## 🔄 Business Logic Flow

### Checklist Workflow

```
1. Login Operatore
   ↓
2. Crea Checklist vuota da Template
   ↓
3. Genera TaskResponse per ogni TaskTemplate
   ↓
4. Operatore completa task
   ↓
5. Update TaskResponse in tempo reale
   ↓
6. Upload foto (se richiesto)
   ↓
7. Validazione task obbligatorie
   ↓
8. Completa Checklist
   ↓
9. Update checklist.completed = true
   ↓
10. Timestamp completed_at
```

### Inventory Update Workflow

```
1. Operatore apre Inventario
   ↓
2. Carica articoli appartamento
   ↓
3. Modifica quantità (+/-)
   ↓
4. Track modifiche in locale
   ↓
5. Click "Salva"
   ↓
6. Per ogni articolo modificato:
   - Crea InventoryHistory record
   - Update quantity
   - Check min_quantity
   - Se quantity ≤ min_quantity:
     → Crea Alert
   ↓
7. Ricarica dati con nuovi alert
```

### Alert Generation Logic

```python
if new_quantity <= min_quantity:
    severity = "high" if new_quantity == 0 else "medium"
    
    alert = Alert(
        apartment_id=item.apartment_id,
        inventory_item_id=item.id,
        alert_type="low_stock",
        message=f"Scorta bassa per {item.name}",
        severity=severity
    )
```

## 🔒 Security Considerations

### Backend

- ✅ **JWT Authentication**: Token-based auth
- ✅ **CORS**: Configurabile per domini specifici
- ✅ **SQL Injection**: Prevenuto da SQLAlchemy ORM
- ✅ **Input Validation**: Pydantic schemas
- ✅ **File Upload**: Validazione tipo e dimensione
- ⏳ **Rate Limiting**: Da implementare (production)
- ⏳ **HTTPS Only**: Da configurare (production)

### Frontend

- ✅ **XSS Protection**: React auto-escaping
- ✅ **Token Storage**: localStorage (migliorabile con httpOnly cookies)
- ✅ **CSRF**: Token in header (non cookie)
- ⏳ **Content Security Policy**: Da configurare

### Raccomandazioni Production

1. **Environment Variables**: Mai committare .env
2. **Secrets Rotation**: Cambia SECRET_KEY periodicamente
3. **Database**: Usa SSL connection
4. **Backups**: Automatici giornalieri
5. **Monitoring**: Sentry, LogRocket, DataDog
6. **Audit Logs**: Traccia azioni critiche

## 📈 Scalability

### Current Limits

- **Users**: Centinaia (non migliaia)
- **Checklists**: Migliaia al mese
- **Inventory Items**: Centinaia per appartamento
- **File Uploads**: 10MB per file

### Scaling Strategies

**Vertical (aumenta risorse server):**
- Più CPU/RAM
- Database più potente
- SSD storage

**Horizontal (quando necessario):**
- Load balancer
- Multiple app servers
- Database replication (read replicas)
- CDN per assets statici
- S3/Cloud storage per upload

## 🧪 Testing Strategy

### Backend Testing

```python
# Unit tests
def test_create_user():
    user = User(name="Test", role="operatore")
    assert user.name == "Test"

# Integration tests  
def test_login_api():
    response = client.post("/api/users/login", json={...})
    assert response.status_code == 200
```

### Frontend Testing

```javascript
// Component tests (React Testing Library)
test('renders login form', () => {
  render(<LoginPage />);
  expect(screen.getByText('Inizia Turno')).toBeInTheDocument();
});

// E2E tests (Playwright/Cypress)
test('complete checklist workflow', async () => {
  await page.goto('/login');
  await page.fill('[name="name"]', 'Test');
  // ...
});
```

## 📊 Monitoring & Analytics

### Metriche da Tracciare

**Backend:**
- Request rate (req/sec)
- Response time (ms)
- Error rate (%)
- Database query time

**Frontend:**
- Page load time
- Time to interactive
- API call duration
- Error tracking

**Business:**
- Checklist completate/giorno
- Tempo medio completamento
- Alert generati
- Articoli riordinati

### Tools Consigliati

- **Application Performance**: New Relic, DataDog
- **Error Tracking**: Sentry
- **Analytics**: Google Analytics, Mixpanel
- **Uptime**: UptimeRobot, Pingdom

---

**Ultimo aggiornamento**: Ottobre 2025  
**Versione**: 1.0.0



