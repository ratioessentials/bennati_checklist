import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { AppProvider, useApp } from './context/AppContext';
import LoginPage from './pages/LoginPage';
import ChecklistPage from './pages/ChecklistPage';
import InventoryPage from './pages/InventoryPage';
import ManagerDashboard from './pages/ManagerDashboard';
import Layout from './components/Layout';
import MobileSimulator from './components/MobileSimulator';

// Protected Route wrapper
const ProtectedRoute = ({ children, requireManager = false }) => {
  const { user, loading } = useApp();

  if (loading) {
    return <div className="spinner"></div>;
  }

  if (!user) {
    return <Navigate to="/" replace />;
  }

  if (requireManager && user.role !== 'manager') {
    return <Navigate to="/checklist" replace />;
  }

  return children;
};

const AppRoutes = () => {
  const { user } = useApp();

  return (
    <Router>
      <Routes>
        {/* Homepage: sempre mostra login */}
        <Route path="/" element={<LoginPage />} />
        
        {/* Pagine protette: solo se loggato */}
        <Route
          path="/checklist"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<ChecklistPage />} />
        </Route>
        
        <Route
          path="/inventory"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<InventoryPage />} />
        </Route>
        
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute requireManager={true}>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<ManagerDashboard />} />
        </Route>

        {/* Redirect per compatibilità */}
        <Route path="/login" element={<Navigate to="/" replace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={true}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </Router>
  );
};

function App() {
  return (
    <AppProvider>
      <MobileSimulator>
        <AppRoutes />
      </MobileSimulator>
    </AppProvider>
  );
}

export default App;



