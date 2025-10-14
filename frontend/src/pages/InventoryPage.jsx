import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { 
  Package, Search, Plus, Minus, AlertTriangle, 
  CheckCircle, Filter, Save 
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { 
  getInventoryItems, updateInventoryItem, 
  getInventoryCategories 
} from '../services/api';

const InventoryPage = () => {
  const { apartment, user } = useApp();
  const [items, setItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showLowStockOnly, setShowLowStockOnly] = useState(false);
  const [changedItems, setChangedItems] = useState({});
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (apartment) {
      loadData();
    }
  }, [apartment]);

  const loadData = async () => {
    try {
      setLoading(true);
      
      const [itemsRes, categoriesRes] = await Promise.all([
        getInventoryItems({ apartment_id: apartment.id }),
        getInventoryCategories()
      ]);
      
      setItems(itemsRes.data);
      setCategories(categoriesRes.data);
    } catch (error) {
      console.error('Errore caricamento inventario:', error);
      toast.error('Errore caricamento inventario');
    } finally {
      setLoading(false);
    }
  };

  const handleQuantityChange = (itemId, newQuantity) => {
    // Aggiorna stato locale
    setItems(items.map(item => 
      item.id === itemId ? { ...item, quantity: newQuantity } : item
    ));
    
    // Traccia cambiamento
    setChangedItems({
      ...changedItems,
      [itemId]: newQuantity
    });
  };

  const incrementQuantity = (item) => {
    handleQuantityChange(item.id, item.quantity + 1);
  };

  const decrementQuantity = (item) => {
    if (item.quantity > 0) {
      handleQuantityChange(item.id, item.quantity - 1);
    }
  };

  const handleSaveChanges = async () => {
    const itemsToUpdate = Object.keys(changedItems);
    
    if (itemsToUpdate.length === 0) {
      toast.info('Nessuna modifica da salvare');
      return;
    }

    try {
      setSaving(true);
      
      // Aggiorna ogni item modificato
      for (const itemId of itemsToUpdate) {
        await updateInventoryItem(itemId, {
          quantity: changedItems[itemId],
          user_id: user.id,
          change_reason: 'Aggiornamento da checklist'
        });
      }
      
      toast.success(`${itemsToUpdate.length} articoli aggiornati`);
      setChangedItems({});
      
      // Ricarica per vedere eventuali alert generati
      await loadData();
    } catch (error) {
      console.error('Errore salvataggio:', error);
      toast.error('Errore salvataggio modifiche');
    } finally {
      setSaving(false);
    }
  };

  const getItemStatus = (item) => {
    if (item.quantity === 0) {
      return { label: 'MANCANTE', color: 'danger', icon: AlertTriangle };
    } else if (item.quantity <= item.min_quantity) {
      return { label: 'BASSO', color: 'warning', icon: AlertTriangle };
    } else {
      return { label: 'OK', color: 'success', icon: CheckCircle };
    }
  };

  // Filtra items
  const filteredItems = items.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || item.category_id === parseInt(selectedCategory);
    const matchesLowStock = !showLowStockOnly || item.quantity <= item.min_quantity;
    
    return matchesSearch && matchesCategory && matchesLowStock;
  });

  // Raggruppa per categoria
  const groupedItems = categories.map(category => ({
    category,
    items: filteredItems.filter(item => item.category_id === category.id)
  })).filter(group => group.items.length > 0);

  if (loading) {
    return <div className="spinner"></div>;
  }

  const hasChanges = Object.keys(changedItems).length > 0;

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="card mb-6">
        <div className="flex items-center gap-3 mb-4">
          <Package size={32} className="text-primary" />
          <div>
            <h2 className="text-2xl font-bold">Inventario</h2>
            <p className="text-gray-600">{apartment?.name}</p>
          </div>
        </div>

        {/* Barra di ricerca e filtri */}
        <div className="space-y-3">
          <div className="relative">
            <Search size={20} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Cerca articolo..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border-2 border-gray-300 rounded-lg"
            />
          </div>

          <div className="flex gap-3">
            <div className="flex-1">
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full p-3 border-2 border-gray-300 rounded-lg"
              >
                <option value="all">Tutte le categorie</option>
                {categories.map(cat => (
                  <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
              </select>
            </div>

            <button
              onClick={() => setShowLowStockOnly(!showLowStockOnly)}
              className={`btn ${showLowStockOnly ? 'btn-warning' : 'btn-outline'}`}
            >
              <Filter size={20} />
              Solo bassi
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-3 mt-4">
          <div className="bg-gray-100 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold">{items.length}</div>
            <div className="text-sm text-gray-600">Totale</div>
          </div>
          <div className="bg-warning bg-opacity-20 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-warning">
              {items.filter(i => i.quantity <= i.min_quantity && i.quantity > 0).length}
            </div>
            <div className="text-sm text-gray-600">Bassi</div>
          </div>
          <div className="bg-danger bg-opacity-20 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-danger">
              {items.filter(i => i.quantity === 0).length}
            </div>
            <div className="text-sm text-gray-600">Mancanti</div>
          </div>
        </div>
      </div>

      {/* Lista articoli raggruppati per categoria */}
      {groupedItems.length === 0 ? (
        <div className="card text-center">
          <p className="text-gray-600">Nessun articolo trovato</p>
        </div>
      ) : (
        <div className="space-y-6">
          {groupedItems.map(({ category, items: categoryItems }) => (
            <div key={category.id}>
              <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
                {category.name}
                {category.is_consumable && (
                  <span className="badge badge-info text-xs">Consumabile</span>
                )}
              </h3>

              <div className="space-y-3">
                {categoryItems.map(item => {
                  const status = getItemStatus(item);
                  const StatusIcon = status.icon;
                  const hasChanged = changedItems.hasOwnProperty(item.id);

                  return (
                    <div 
                      key={item.id} 
                      className={`card ${hasChanged ? 'ring-2 ring-primary' : ''}`}
                    >
                      <div className="flex items-center justify-between gap-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h4 className="font-semibold">{item.name}</h4>
                            <span className={`badge badge-${status.color} flex items-center gap-1`}>
                              <StatusIcon size={14} />
                              {status.label}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600">
                            Min: {item.min_quantity} {item.unit}
                          </p>
                        </div>

                        {/* Controlli quantità */}
                        <div className="flex items-center gap-3">
                          <button
                            onClick={() => decrementQuantity(item)}
                            className="btn btn-outline w-12 h-12 p-0"
                            disabled={item.quantity === 0}
                          >
                            <Minus size={20} />
                          </button>

                          <div className="text-center min-w-[80px]">
                            <div className="text-2xl font-bold">{item.quantity}</div>
                            <div className="text-xs text-gray-600">{item.unit}</div>
                          </div>

                          <button
                            onClick={() => incrementQuantity(item)}
                            className="btn btn-secondary w-12 h-12 p-0"
                          >
                            <Plus size={20} />
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pulsante salva modifiche */}
      {hasChanges && (
        <div className="fixed bottom-0 left-0 right-0 p-4 bg-white shadow-lg border-t-4 border-primary z-50">
          <div className="max-w-4xl mx-auto">
            <button
              onClick={handleSaveChanges}
              className="btn btn-primary w-full"
              disabled={saving}
            >
              {saving ? (
                <>
                  <div className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }}></div>
                  Salvataggio...
                </>
              ) : (
                <>
                  <Save size={24} />
                  Salva {Object.keys(changedItems).length} Modifiche
                </>
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default InventoryPage;



