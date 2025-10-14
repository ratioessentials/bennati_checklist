import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor per aggiungere token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Users & Auth
export const login = (data) => api.post('/api/users/login', data);
export const getUsers = () => api.get('/api/users/');
export const createUser = (data) => api.post('/api/users/', data);

// Apartments
export const getApartments = () => api.get('/api/apartments/');
export const getApartment = (id) => api.get(`/api/apartments/${id}`);
export const createApartment = (data) => api.post('/api/apartments/', data);
export const updateApartment = (id, data) => api.put(`/api/apartments/${id}`, data);

// Checklists
export const getChecklists = (params) => api.get('/api/checklists/', { params });
export const getChecklist = (id) => api.get(`/api/checklists/${id}`);
export const createChecklist = (data) => api.post('/api/checklists/', data);
export const updateChecklist = (id, data) => api.put(`/api/checklists/${id}`, data);
export const getChecklistTasks = (checklistId) => api.get(`/api/checklists/${checklistId}/tasks`);
export const updateTaskResponse = (taskId, data) => api.put(`/api/checklists/tasks/${taskId}`, data);
export const uploadTaskPhoto = (taskId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post(`/api/checklists/tasks/${taskId}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Templates
export const getTemplates = (params) => api.get('/api/checklists/templates/', { params });
export const getTemplate = (id) => api.get(`/api/checklists/templates/${id}`);
export const createTemplate = (data) => api.post('/api/checklists/templates/', data);

// Inventory
export const getInventoryCategories = () => api.get('/api/inventory/categories');
export const createInventoryCategory = (data) => api.post('/api/inventory/categories', data);
export const getInventoryItems = (params) => api.get('/api/inventory/items', { params });
export const getInventoryItem = (id) => api.get(`/api/inventory/items/${id}`);
export const createInventoryItem = (data) => api.post('/api/inventory/items', data);
export const updateInventoryItem = (id, data) => api.put(`/api/inventory/items/${id}`, data);
export const getItemHistory = (id) => api.get(`/api/inventory/items/${id}/history`);

// Alerts
export const getAlerts = (params) => api.get('/api/inventory/alerts', { params });
export const createAlert = (data) => api.post('/api/inventory/alerts', data);
export const resolveAlert = (id) => api.put(`/api/inventory/alerts/${id}/resolve`);

// Reports
export const getManagerDashboard = () => api.get('/api/reports/dashboard');
export const getApartmentInventoryReport = (id) => api.get(`/api/reports/apartment/${id}/inventory`);
export const getApartmentStatistics = (id) => api.get(`/api/reports/stats/apartment/${id}`);
export const exportInventoryPDF = (apartmentId) => 
  api.get('/api/reports/export/inventory/pdf', { 
    params: { apartment_id: apartmentId },
    responseType: 'blob'
  });
export const exportInventoryCSV = (apartmentId) => 
  api.get('/api/reports/export/inventory/csv', { 
    params: { apartment_id: apartmentId },
    responseType: 'blob'
  });
export const exportChecklistsCSV = (params) => 
  api.get('/api/reports/export/checklists/csv', { 
    params,
    responseType: 'blob'
  });

export default api;



