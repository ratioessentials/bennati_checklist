import React from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Home, Package, BarChart3, LogOut, Menu, X } from 'lucide-react';

const Layout = () => {
  const { user, apartment, logout } = useApp();
  const location = useLocation();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = React.useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { path: '/', icon: Home, label: 'Checklist', roles: ['operatore', 'manager'] },
    { path: '/inventory', icon: Package, label: 'Inventario', roles: ['operatore', 'manager'] },
    { path: '/dashboard', icon: BarChart3, label: 'Dashboard', roles: ['manager'] },
  ];

  const filteredNavItems = navItems.filter(item => 
    item.roles.includes(user?.role)
  );

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-primary text-white shadow-lg sticky top-0 z-50">
        <div className="container">
          <div className="flex items-center justify-between py-4">
            <div>
              <h1 className="text-xl font-bold">Bennati Checklist</h1>
              {apartment && (
                <p className="text-sm opacity-90">{apartment.name}</p>
              )}
            </div>
            
            {/* Mobile menu button */}
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="lg:hidden p-2"
              aria-label="Menu"
            >
              {menuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>

            {/* Desktop user info */}
            <div className="hidden lg:flex items-center gap-4">
              <div className="text-right">
                <p className="font-semibold">{user?.name}</p>
                <p className="text-sm opacity-90 capitalize">{user?.role}</p>
              </div>
              <button
                onClick={handleLogout}
                className="btn btn-outline border-white text-white hover:bg-white hover:text-primary"
              >
                <LogOut size={20} />
                Esci
              </button>
            </div>
          </div>

          {/* Mobile menu */}
          {menuOpen && (
            <div className="lg:hidden pb-4">
              <div className="bg-primary-dark rounded-lg p-4 mb-3">
                <p className="font-semibold">{user?.name}</p>
                <p className="text-sm opacity-90 capitalize">{user?.role}</p>
              </div>
              <button
                onClick={handleLogout}
                className="btn w-full btn-outline border-white text-white hover:bg-white hover:text-primary"
              >
                <LogOut size={20} />
                Esci
              </button>
            </div>
          )}
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-md sticky top-[72px] lg:top-[80px] z-40">
        <div className="container">
          <div className="flex overflow-x-auto">
            {filteredNavItems.map(({ path, icon: Icon, label }) => {
              const isActive = location.pathname === path;
              return (
                <Link
                  key={path}
                  to={path}
                  className={`flex items-center gap-2 px-6 py-4 font-semibold whitespace-nowrap transition-colors ${
                    isActive
                      ? 'text-primary border-b-4 border-primary'
                      : 'text-gray-600 hover:text-primary'
                  }`}
                >
                  <Icon size={20} />
                  {label}
                </Link>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main content */}
      <main className="flex-1 container py-6">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-4 mt-8">
        <div className="container text-center">
          <p className="text-sm">
            &copy; {new Date().getFullYear()} Bennati Checklist - Gestione Pulizie Appartamenti
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;



