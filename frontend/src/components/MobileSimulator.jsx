import React, { useState } from 'react';
import { Smartphone, Monitor, RotateCcw } from 'lucide-react';

const MobileSimulator = ({ children }) => {
  const [isSimulating, setIsSimulating] = useState(true);
  const [orientation, setOrientation] = useState('portrait'); // portrait o landscape

  // Dimensioni smartphone tipiche
  const mobileDimensions = {
    portrait: { width: '375px', height: '667px' }, // iPhone SE
    landscape: { width: '667px', height: '375px' }
  };

  const currentDimensions = mobileDimensions[orientation];

  const toggleSimulation = () => {
    setIsSimulating(!isSimulating);
  };

  const toggleOrientation = () => {
    setOrientation(orientation === 'portrait' ? 'landscape' : 'portrait');
  };

  if (!isSimulating) {
    return (
      <div className="min-h-screen">
        {children}
        {/* Floating toggle button */}
        <button
          onClick={toggleSimulation}
          className="fixed top-4 right-4 z-50 bg-primary text-white p-3 rounded-full shadow-lg hover:bg-primary-dark transition-colors"
          title="Attiva simulazione mobile"
        >
          <Smartphone size={24} />
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      {/* Controlli */}
      <div className="fixed top-4 left-4 z-50 flex gap-2">
        <button
          onClick={toggleSimulation}
          className="simulator-control glass-effect text-gray-700 p-2 rounded-lg shadow-lg hover:bg-gray-50"
          title="Disattiva simulazione mobile"
        >
          <Monitor size={20} />
        </button>
        <button
          onClick={toggleOrientation}
          className="simulator-control glass-effect text-gray-700 p-2 rounded-lg shadow-lg hover:bg-gray-50"
          title={`Ruota in ${orientation === 'portrait' ? 'landscape' : 'portrait'}`}
        >
          <RotateCcw size={20} />
        </button>
      </div>

      {/* Info */}
      <div className="fixed top-4 right-4 z-50 glass-effect text-gray-600 px-3 py-2 rounded-lg shadow-lg text-sm">
        <div className="flex items-center gap-2">
          <Smartphone size={16} />
          <span>
            {orientation === 'portrait' ? 'Portrait' : 'Landscape'} • 
            {currentDimensions.width} × {currentDimensions.height}
          </span>
        </div>
      </div>

      {/* Simulatore mobile */}
      <div className="relative">
        {/* Cornice del telefono */}
        <div 
          className="bg-black rounded-[2.5rem] p-2 shadow-2xl"
          style={{
            width: `calc(${currentDimensions.width} + 16px)`,
            height: `calc(${currentDimensions.height} + 16px)`
          }}
        >
          {/* Schermo */}
          <div 
            className="bg-white rounded-[2rem] overflow-hidden relative"
            style={{
              width: currentDimensions.width,
              height: currentDimensions.height
            }}
          >
            {/* Notch (solo in portrait) */}
            {orientation === 'portrait' && (
              <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-32 h-6 bg-black rounded-b-2xl z-10"></div>
            )}
            
            {/* Contenuto dell'app */}
            <div 
              className="w-full h-full overflow-auto mobile-simulator"
              style={{
                width: currentDimensions.width,
                height: currentDimensions.height
              }}
            >
              {children}
            </div>
          </div>
        </div>

        {/* Indicatori di orientamento */}
        <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 text-gray-500 text-sm">
          📱 Simulazione Mobile
        </div>
      </div>

      {/* Istruzioni */}
      <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 glass-effect text-gray-600 px-4 py-2 rounded-lg shadow-lg text-sm">
        <div className="flex items-center gap-4">
          <span>🖱️ Clicca Monitor per uscire dalla simulazione</span>
          <span>🔄 Clicca Rotate per cambiare orientamento</span>
        </div>
      </div>
    </div>
  );
};

export default MobileSimulator;
