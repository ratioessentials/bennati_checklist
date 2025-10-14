import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { LogIn, Building2, Calendar, User } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { login, getApartments } from '../services/api';

const LoginPage = () => {
  const navigate = useNavigate();
  const { loginUser } = useApp();
  const [loading, setLoading] = useState(false);
  const [apartments, setApartments] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    apartment_id: '',
    date: new Date().toISOString().split('T')[0],
  });

  useEffect(() => {
    fetchApartments();
  }, []);

  const fetchApartments = async () => {
    try {
      const response = await getApartments();
      setApartments(response.data);
    } catch (error) {
      console.error('Errore nel caricamento appartamenti:', error);
      toast.error('Errore nel caricamento appartamenti');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name.trim()) {
      toast.error('Inserisci il tuo nome');
      return;
    }
    
    if (!formData.apartment_id) {
      toast.error('Seleziona un appartamento');
      return;
    }

    setLoading(true);
    
    try {
      const response = await login({
        name: formData.name.trim(),
        apartment_id: parseInt(formData.apartment_id),
        date: formData.date ? new Date(formData.date).toISOString() : null,
      });

      const { user, apartment, checklist, access_token } = response.data;
      
      loginUser(user, apartment, checklist, access_token);
      
      toast.success(`Benvenuta/o ${user.name}!`);
      navigate('/');
    } catch (error) {
      console.error('Errore login:', error);
      toast.error('Errore durante il login. Riprova.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary to-primary-dark p-4">
      <div className="w-full max-w-md">
        <div className="card shadow-2xl">
          <div className="text-center mb-8">
            <div className="inline-block p-4 bg-primary rounded-full mb-4">
              <Building2 size={48} className="text-white" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Bennati Checklist
            </h1>
            <p className="text-gray-600">
              Gestione pulizie appartamenti
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="input-group">
              <label htmlFor="name">
                <User size={20} className="inline mr-2" />
                Nome Operatore
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Inserisci il tuo nome"
                autoComplete="name"
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="apartment_id">
                <Building2 size={20} className="inline mr-2" />
                Appartamento
              </label>
              <select
                id="apartment_id"
                name="apartment_id"
                value={formData.apartment_id}
                onChange={handleChange}
                required
              >
                <option value="">Seleziona appartamento</option>
                {apartments.map((apt) => (
                  <option key={apt.id} value={apt.id}>
                    {apt.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="input-group">
              <label htmlFor="date">
                <Calendar size={20} className="inline mr-2" />
                Data
              </label>
              <input
                type="date"
                id="date"
                name="date"
                value={formData.date}
                onChange={handleChange}
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary w-full"
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }}></div>
                  Accesso in corso...
                </>
              ) : (
                <>
                  <LogIn size={20} />
                  Inizia Turno
                </>
              )}
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-gray-200 text-center text-sm text-gray-600">
            <p>Seleziona il tuo nome e l'appartamento su cui lavorerai oggi</p>
          </div>
        </div>

        <div className="text-center mt-4 text-white">
          <p className="text-sm opacity-90">
            v1.0.0 - Mobile First Design
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;



