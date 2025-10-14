import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { 
  BarChart3, Building2, Package, AlertTriangle, 
  CheckCircle, FileDown, Calendar, TrendingDown,
  ClipboardCheck, Bell
} from 'lucide-react';
import { 
  getManagerDashboard, exportInventoryCSV, 
  exportInventoryPDF, getApartmentStatistics 
} from '../services/api';

const ManagerDashboard = () => {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedApartment, setSelectedApartment] = useState(null);
  const [apartmentStats, setApartmentStats] = useState(null);
  const [loadingStats, setLoadingStats] = useState(false);

  useEffect(() => {
    loadDashboard();
  }, []);

  useEffect(() => {
    if (selectedApartment) {
      loadApartmentStats(selectedApartment);
    }
  }, [selectedApartment]);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const response = await getManagerDashboard();
      setDashboard(response.data);
    } catch (error) {
      console.error('Errore caricamento dashboard:', error);
      toast.error('Errore caricamento dashboard');
    } finally {
      setLoading(false);
    }
  };

  const loadApartmentStats = async (apartmentId) => {
    try {
      setLoadingStats(true);
      const response = await getApartmentStatistics(apartmentId);
      setApartmentStats(response.data);
    } catch (error) {
      console.error('Errore caricamento statistiche:', error);
      toast.error('Errore caricamento statistiche');
    } finally {
      setLoadingStats(false);
    }
  };

  const handleExportPDF = async (apartmentId) => {
    try {
      toast.info('Generazione PDF...');
      const response = await exportInventoryPDF(apartmentId);
      
      // Crea link download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `inventario_apt${apartmentId}_${new Date().toISOString().split('T')[0]}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('PDF scaricato');
    } catch (error) {
      console.error('Errore export PDF:', error);
      toast.error('Errore export PDF');
    }
  };

  const handleExportCSV = async (apartmentId = null) => {
    try {
      toast.info('Generazione CSV...');
      const response = await exportInventoryCSV(apartmentId);
      
      // Crea link download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `inventario${apartmentId ? `_apt${apartmentId}` : '_tutti'}_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('CSV scaricato');
    } catch (error) {
      console.error('Errore export CSV:', error);
      toast.error('Errore export CSV');
    }
  };

  if (loading) {
    return <div className="spinner"></div>;
  }

  if (!dashboard) {
    return (
      <div className="card text-center">
        <p className="text-gray-600">Errore caricamento dashboard</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="card mb-6">
        <div className="flex items-center gap-3 mb-4">
          <BarChart3 size={32} className="text-primary" />
          <div>
            <h2 className="text-2xl font-bold">Dashboard Manager</h2>
            <p className="text-gray-600">Panoramica completa di tutti gli appartamenti</p>
          </div>
        </div>

        {/* Stats generali */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <div className="bg-primary bg-opacity-10 rounded-lg p-4 text-center">
            <Building2 size={24} className="mx-auto mb-2 text-primary" />
            <div className="text-2xl font-bold">{dashboard.apartments?.length || 0}</div>
            <div className="text-sm text-gray-600">Appartamenti</div>
          </div>
          
          <div className="bg-danger bg-opacity-10 rounded-lg p-4 text-center">
            <AlertTriangle size={24} className="mx-auto mb-2 text-danger" />
            <div className="text-2xl font-bold">{dashboard.active_alerts?.length || 0}</div>
            <div className="text-sm text-gray-600">Alert Attivi</div>
          </div>
          
          <div className="bg-warning bg-opacity-10 rounded-lg p-4 text-center">
            <TrendingDown size={24} className="mx-auto mb-2 text-warning" />
            <div className="text-2xl font-bold">{dashboard.items_to_restock?.length || 0}</div>
            <div className="text-sm text-gray-600">Da Riordinare</div>
          </div>
          
          <div className="bg-secondary bg-opacity-10 rounded-lg p-4 text-center">
            <ClipboardCheck size={24} className="mx-auto mb-2 text-secondary" />
            <div className="text-2xl font-bold">{dashboard.recent_checklists?.length || 0}</div>
            <div className="text-sm text-gray-600">Checklist (7gg)</div>
          </div>
        </div>

        {/* Export globale */}
        <div className="mt-4 flex gap-3">
          <button
            onClick={() => handleExportCSV(null)}
            className="btn btn-primary flex-1"
          >
            <FileDown size={20} />
            Esporta Tutto (CSV)
          </button>
        </div>
      </div>

      {/* Alert attivi */}
      {dashboard.active_alerts && dashboard.active_alerts.length > 0 && (
        <div className="card mb-6">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Bell size={24} className="text-danger" />
            Alert Attivi
          </h3>
          <div className="space-y-2">
            {dashboard.active_alerts.slice(0, 5).map((alert) => (
              <div 
                key={alert.id} 
                className={`p-3 rounded-lg border-l-4 ${
                  alert.severity === 'high' ? 'border-danger bg-danger bg-opacity-10' :
                  alert.severity === 'medium' ? 'border-warning bg-warning bg-opacity-10' :
                  'border-gray-400 bg-gray-100'
                }`}
              >
                <div className="flex items-start gap-2">
                  <AlertTriangle size={20} className={
                    alert.severity === 'high' ? 'text-danger' : 'text-warning'
                  } />
                  <div className="flex-1">
                    <p className="font-semibold">{alert.message}</p>
                    <p className="text-sm text-gray-600">
                      {new Date(alert.created_at).toLocaleString('it-IT')}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Lista appartamenti */}
      <div className="grid lg:grid-cols-2 gap-6 mb-6">
        {dashboard.apartments?.map((apt) => (
          <div 
            key={apt.apartment.id} 
            className="card hover:shadow-xl transition-shadow cursor-pointer"
            onClick={() => setSelectedApartment(apt.apartment.id)}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <Building2 size={28} className="text-primary" />
                <div>
                  <h3 className="text-xl font-bold">{apt.apartment.name}</h3>
                  <p className="text-sm text-gray-600">{apt.total_items} articoli totali</p>
                </div>
              </div>
              
              {(apt.low_stock_items.length > 0 || apt.missing_items.length > 0) && (
                <AlertTriangle size={24} className="text-warning" />
              )}
            </div>

            {/* Stats appartamento */}
            <div className="grid grid-cols-2 gap-3 mb-4">
              <div className="bg-warning bg-opacity-20 rounded p-3 text-center">
                <div className="text-xl font-bold text-warning">
                  {apt.low_stock_items.length}
                </div>
                <div className="text-xs text-gray-600">Scorta Bassa</div>
              </div>
              <div className="bg-danger bg-opacity-20 rounded p-3 text-center">
                <div className="text-xl font-bold text-danger">
                  {apt.missing_items.length}
                </div>
                <div className="text-xs text-gray-600">Mancanti</div>
              </div>
            </div>

            {/* Articoli da riordinare */}
            {(apt.low_stock_items.length > 0 || apt.missing_items.length > 0) && (
              <div className="border-t pt-3">
                <h4 className="font-semibold text-sm mb-2">Da riordinare:</h4>
                <div className="space-y-1">
                  {[...apt.missing_items, ...apt.low_stock_items].slice(0, 3).map((item) => (
                    <div key={item.id} className="flex justify-between text-sm">
                      <span>{item.name}</span>
                      <span className={`font-semibold ${item.quantity === 0 ? 'text-danger' : 'text-warning'}`}>
                        {item.quantity} {item.unit}
                      </span>
                    </div>
                  ))}
                  {(apt.low_stock_items.length + apt.missing_items.length) > 3 && (
                    <p className="text-xs text-gray-600">
                      +{(apt.low_stock_items.length + apt.missing_items.length) - 3} altri...
                    </p>
                  )}
                </div>
              </div>
            )}

            {/* Azioni */}
            <div className="flex gap-2 mt-4">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleExportPDF(apt.apartment.id);
                }}
                className="btn btn-outline flex-1 text-sm"
              >
                <FileDown size={16} />
                PDF
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleExportCSV(apt.apartment.id);
                }}
                className="btn btn-outline flex-1 text-sm"
              >
                <FileDown size={16} />
                CSV
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Statistiche appartamento selezionato */}
      {selectedApartment && (
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-bold">
              Statistiche Dettagliate
            </h3>
            <button
              onClick={() => setSelectedApartment(null)}
              className="btn btn-outline"
            >
              Chiudi
            </button>
          </div>

          {loadingStats ? (
            <div className="spinner"></div>
          ) : apartmentStats ? (
            <div>
              <h4 className="font-semibold mb-3">{apartmentStats.apartment.name}</h4>
              
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
                <div className="bg-gray-100 rounded p-3">
                  <div className="text-sm text-gray-600">Checklist Totali</div>
                  <div className="text-2xl font-bold">{apartmentStats.total_checklists}</div>
                </div>
                <div className="bg-secondary bg-opacity-20 rounded p-3">
                  <div className="text-sm text-gray-600">Completate</div>
                  <div className="text-2xl font-bold text-secondary">
                    {apartmentStats.completed_checklists}
                  </div>
                </div>
                <div className="bg-primary bg-opacity-20 rounded p-3">
                  <div className="text-sm text-gray-600">Tasso Completamento</div>
                  <div className="text-2xl font-bold text-primary">
                    {Math.round(apartmentStats.completion_rate)}%
                  </div>
                </div>
                <div className="bg-warning bg-opacity-20 rounded p-3">
                  <div className="text-sm text-gray-600">Ultimi 30gg</div>
                  <div className="text-2xl font-bold text-warning">
                    {apartmentStats.recent_checklists_30d}
                  </div>
                </div>
              </div>
            </div>
          ) : null}
        </div>
      )}

      {/* Lista completa articoli da riordinare */}
      {dashboard.items_to_restock && dashboard.items_to_restock.length > 0 && (
        <div className="card mt-6">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Package size={24} className="text-warning" />
            Tutti gli Articoli da Riordinare
          </h3>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100">
                <tr>
                  <th className="text-left p-3">Articolo</th>
                  <th className="text-left p-3">Appartamento</th>
                  <th className="text-center p-3">Quantità</th>
                  <th className="text-center p-3">Minimo</th>
                  <th className="text-center p-3">Stato</th>
                </tr>
              </thead>
              <tbody>
                {dashboard.items_to_restock.map((item) => (
                  <tr key={`${item.apartment_id}-${item.id}`} className="border-b">
                    <td className="p-3 font-semibold">{item.name}</td>
                    <td className="p-3 text-sm text-gray-600">
                      {dashboard.apartments.find(a => a.apartment.id === item.apartment_id)?.apartment.name}
                    </td>
                    <td className="p-3 text-center">
                      <span className={`font-bold ${item.quantity === 0 ? 'text-danger' : 'text-warning'}`}>
                        {item.quantity} {item.unit}
                      </span>
                    </td>
                    <td className="p-3 text-center text-gray-600">
                      {item.min_quantity} {item.unit}
                    </td>
                    <td className="p-3 text-center">
                      <span className={`badge ${item.quantity === 0 ? 'badge-danger' : 'badge-warning'}`}>
                        {item.quantity === 0 ? 'MANCANTE' : 'BASSO'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default ManagerDashboard;



