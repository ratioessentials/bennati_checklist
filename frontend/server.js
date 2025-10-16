const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Serve pages
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/select', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'select.html'));
});

app.get('/checklist', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'checklist.html'));
});

// Helper function to call backend
async function callBackend(endpoint, options = {}) {
    const response = await fetch(`http://backend:8000${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    });
    return response;
}

// API endpoints
app.post('/api/login', async (req, res) => {
    try {
        const response = await callBackend('/api/login', {
            method: 'POST',
            body: JSON.stringify(req.body)
        });
        
        const data = await response.json();
        res.status(response.status).json(data);
    } catch (error) {
        res.status(500).json({ error: 'Errore di connessione al server' });
    }
});

app.get('/api/apartments', async (req, res) => {
    try {
        const response = await callBackend('/api/apartments', {
            method: 'GET',
            headers: {
                'Authorization': req.headers.authorization
            }
        });
        
        const data = await response.json();
        res.status(response.status).json(data);
    } catch (error) {
        res.status(500).json({ error: 'Errore di connessione al server' });
    }
});

app.post('/api/checklists', async (req, res) => {
    try {
        const response = await callBackend('/api/checklists', {
            method: 'POST',
            headers: {
                'Authorization': req.headers.authorization
            },
            body: JSON.stringify(req.body)
        });
        
        const data = await response.json();
        res.status(response.status).json(data);
    } catch (error) {
        res.status(500).json({ error: 'Errore di connessione al server' });
    }
});

app.get('/api/checklists/:id', async (req, res) => {
    try {
        const response = await callBackend(`/api/checklists/${req.params.id}`, {
            method: 'GET',
            headers: {
                'Authorization': req.headers.authorization
            }
        });
        
        const data = await response.json();
        res.status(response.status).json(data);
    } catch (error) {
        res.status(500).json({ error: 'Errore di connessione al server' });
    }
});

app.patch('/api/tasks/:id/complete', async (req, res) => {
    try {
        const response = await callBackend(`/api/tasks/${req.params.id}/complete`, {
            method: 'PATCH',
            headers: {
                'Authorization': req.headers.authorization
            },
            body: JSON.stringify(req.body)
        });
        
        const data = await response.json();
        res.status(response.status).json(data);
    } catch (error) {
        res.status(500).json({ error: 'Errore di connessione al server' });
    }
});

app.patch('/api/checklists/:id/complete', async (req, res) => {
    try {
        const response = await callBackend(`/api/checklists/${req.params.id}/complete`, {
            method: 'PATCH',
            headers: {
                'Authorization': req.headers.authorization
            }
        });
        
        const data = await response.json();
        res.status(response.status).json(data);
    } catch (error) {
        res.status(500).json({ error: 'Errore di connessione al server' });
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Frontend server running on port ${PORT}`);
});
