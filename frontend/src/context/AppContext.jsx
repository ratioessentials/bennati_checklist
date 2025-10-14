import React, { createContext, useContext, useState, useEffect } from 'react';

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp deve essere usato all\'interno di AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [apartment, setApartment] = useState(null);
  const [checklist, setChecklist] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Recupera dati da localStorage all'avvio
    const savedUser = localStorage.getItem('user');
    const savedApartment = localStorage.getItem('apartment');
    const savedChecklist = localStorage.getItem('checklist');
    const token = localStorage.getItem('token');

    if (savedUser && token) {
      setUser(JSON.parse(savedUser));
    }
    if (savedApartment) {
      setApartment(JSON.parse(savedApartment));
    }
    if (savedChecklist) {
      setChecklist(JSON.parse(savedChecklist));
    }
    setLoading(false);
  }, []);

  const loginUser = (userData, apartmentData, checklistData, token) => {
    setUser(userData);
    setApartment(apartmentData);
    setChecklist(checklistData);
    
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('apartment', JSON.stringify(apartmentData));
    localStorage.setItem('checklist', JSON.stringify(checklistData));
    localStorage.setItem('token', token);
  };

  const logout = () => {
    setUser(null);
    setApartment(null);
    setChecklist(null);
    
    localStorage.removeItem('user');
    localStorage.removeItem('apartment');
    localStorage.removeItem('checklist');
    localStorage.removeItem('token');
  };

  const updateChecklist = (checklistData) => {
    setChecklist(checklistData);
    localStorage.setItem('checklist', JSON.stringify(checklistData));
  };

  const value = {
    user,
    apartment,
    checklist,
    loading,
    loginUser,
    logout,
    updateChecklist,
    isOperatore: user?.role === 'operatore',
    isManager: user?.role === 'manager',
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};



