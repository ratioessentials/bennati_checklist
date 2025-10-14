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

// Protected Route wrapper
const ProtectedRoute = ({ children, requireManager = false }) => {
  const { user, loading } = useApp();

  if (loading) {
    return <div className="spinner"></div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (requireManager && user.role !== 'manager') {
    return <Navigate to="/" replace />;
  }

  return children;
};

const AppRoutes = () => {
  const { user } = useApp();

  return (
    <Router>
      <Routes>
        <Route path="/login" element={user ? <Navigate to="/" replace /> : <LoginPage />} />
        
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<ChecklistPage />} />
          <Route path="inventory" element={<InventoryPage />} />
          <Route
            path="dashboard"
            element={
              <ProtectedRoute requireManager={true}>
                <ManagerDashboard />
              </ProtectedRoute>
            }
          />
        </Route>

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
      <AppRoutes />
    </AppProvider>
  );
}

export default App;



