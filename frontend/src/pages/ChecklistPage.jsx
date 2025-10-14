import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { 
  CheckCircle2, Circle, Camera, FileText, Save, 
  CheckSquare, AlignLeft, HelpCircle, Image 
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { 
  getChecklist, updateChecklist, updateTaskResponse, 
  uploadTaskPhoto 
} from '../services/api';

const ChecklistPage = () => {
  const { checklist: contextChecklist, updateChecklist: updateContextChecklist } = useApp();
  const [checklist, setChecklist] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notes, setNotes] = useState('');

  useEffect(() => {
    if (contextChecklist) {
      loadChecklist();
    }
  }, [contextChecklist]);

  const loadChecklist = async () => {
    try {
      setLoading(true);
      const response = await getChecklist(contextChecklist.id);
      const data = response.data;
      
      setChecklist(data);
      setTasks(data.task_responses || []);
      setNotes(data.notes || '');
    } catch (error) {
      console.error('Errore nel caricamento checklist:', error);
      toast.error('Errore nel caricamento checklist');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskUpdate = async (taskId, updates) => {
    try {
      const response = await updateTaskResponse(taskId, updates);
      
      // Aggiorna task nella lista
      setTasks(tasks.map(t => 
        t.id === taskId ? { ...t, ...response.data } : t
      ));
      
      toast.success('Task aggiornata');
    } catch (error) {
      console.error('Errore aggiornamento task:', error);
      toast.error('Errore aggiornamento task');
    }
  };

  const handlePhotoUpload = async (taskId, file) => {
    if (!file) return;

    // Verifica dimensione file (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('File troppo grande. Massimo 10MB');
      return;
    }

    try {
      toast.info('Caricamento in corso...');
      await uploadTaskPhoto(taskId, file);
      
      // Ricarica checklist per vedere foto aggiornate
      await loadChecklist();
      
      toast.success('Foto caricata con successo');
    } catch (error) {
      console.error('Errore caricamento foto:', error);
      toast.error('Errore caricamento foto');
    }
  };

  const handleCompleteChecklist = async () => {
    // Verifica che tutte le task obbligatorie siano completate
    const requiredTasks = tasks.filter(t => t.task_template?.required);
    const incompleteRequired = requiredTasks.filter(t => !t.completed);
    
    if (incompleteRequired.length > 0) {
      toast.error(`Completa tutte le task obbligatorie (${incompleteRequired.length} rimanenti)`);
      return;
    }

    try {
      setSaving(true);
      
      // Aggiorna note
      await updateChecklist(checklist.id, {
        completed: true,
        notes: notes
      });
      
      toast.success('Checklist completata! 🎉');
      
      // Aggiorna context
      const response = await getChecklist(checklist.id);
      updateContextChecklist(response.data);
      
      // Ricarica
      await loadChecklist();
    } catch (error) {
      console.error('Errore completamento checklist:', error);
      toast.error('Errore completamento checklist');
    } finally {
      setSaving(false);
    }
  };

  const handleSaveNotes = async () => {
    try {
      await updateChecklist(checklist.id, { notes });
      toast.success('Note salvate');
    } catch (error) {
      console.error('Errore salvataggio note:', error);
      toast.error('Errore salvataggio note');
    }
  };

  const getTaskIcon = (taskType) => {
    switch (taskType) {
      case 'checkbox':
        return CheckSquare;
      case 'text':
        return AlignLeft;
      case 'yes_no':
        return HelpCircle;
      case 'photo':
        return Camera;
      default:
        return Circle;
    }
  };

  if (loading) {
    return <div className="spinner"></div>;
  }

  if (!checklist) {
    return (
      <div className="card text-center">
        <p className="text-gray-600">Nessuna checklist trovata</p>
      </div>
    );
  }

  const completedTasks = tasks.filter(t => t.completed).length;
  const totalTasks = tasks.length;
  const progress = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header con progresso */}
      <div className="card mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Checklist Pulizia</h2>
          {checklist.completed && (
            <span className="badge badge-success">
              <CheckCircle2 size={16} className="mr-1" />
              Completata
            </span>
          )}
        </div>
        
        <div className="mb-2">
          <div className="flex justify-between text-sm mb-1">
            <span className="font-semibold">Progresso</span>
            <span className="text-gray-600">
              {completedTasks} di {totalTasks} task completate
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-secondary h-3 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Task list */}
      <div className="space-y-4">
        {tasks.map((task) => {
          const Icon = getTaskIcon(task.task_template?.task_type);
          const isRequired = task.task_template?.required;
          
          return (
            <div key={task.id} className="card">
              <div className="flex items-start gap-3">
                <button
                  onClick={() => handleTaskUpdate(task.id, { 
                    completed: !task.completed 
                  })}
                  className="mt-1 flex-shrink-0"
                  disabled={checklist.completed}
                >
                  {task.completed ? (
                    <CheckCircle2 size={24} className="text-secondary" />
                  ) : (
                    <Circle size={24} className="text-gray-400" />
                  )}
                </button>

                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <Icon size={18} className="text-gray-600" />
                    <h3 className="font-semibold">
                      {task.task_template?.title}
                      {isRequired && <span className="text-danger ml-1">*</span>}
                    </h3>
                  </div>

                  {task.task_template?.description && (
                    <p className="text-sm text-gray-600 mb-3">
                      {task.task_template.description}
                    </p>
                  )}

                  {/* Task type specific inputs */}
                  {task.task_template?.task_type === 'text' && (
                    <textarea
                      className="w-full p-3 border-2 border-gray-300 rounded-lg"
                      rows="3"
                      placeholder="Inserisci note..."
                      value={task.text_response || ''}
                      onChange={(e) => handleTaskUpdate(task.id, {
                        text_response: e.target.value
                      })}
                      disabled={checklist.completed}
                    />
                  )}

                  {task.task_template?.task_type === 'yes_no' && (
                    <div className="flex gap-3">
                      <button
                        onClick={() => handleTaskUpdate(task.id, {
                          yes_no_response: true
                        })}
                        className={`btn flex-1 ${
                          task.yes_no_response === true
                            ? 'btn-secondary'
                            : 'btn-outline'
                        }`}
                        disabled={checklist.completed}
                      >
                        Sì
                      </button>
                      <button
                        onClick={() => handleTaskUpdate(task.id, {
                          yes_no_response: false
                        })}
                        className={`btn flex-1 ${
                          task.yes_no_response === false
                            ? 'btn-danger'
                            : 'btn-outline'
                        }`}
                        disabled={checklist.completed}
                      >
                        No
                      </button>
                    </div>
                  )}

                  {task.task_template?.task_type === 'photo' && (
                    <div>
                      <input
                        type="file"
                        accept="image/*,video/*"
                        capture="environment"
                        id={`photo-${task.id}`}
                        className="hidden"
                        onChange={(e) => {
                          if (e.target.files[0]) {
                            handlePhotoUpload(task.id, e.target.files[0]);
                          }
                        }}
                        disabled={checklist.completed}
                      />
                      <label
                        htmlFor={`photo-${task.id}`}
                        className={`btn btn-primary ${checklist.completed ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                      >
                        <Camera size={20} />
                        Carica Foto/Video
                      </label>

                      {/* Mostra foto caricate */}
                      {task.photo_paths && (
                        <div className="mt-3 grid grid-cols-2 gap-2">
                          {JSON.parse(task.photo_paths).map((photo, idx) => (
                            <div key={idx} className="relative">
                              <img
                                src={`/uploads/${photo}`}
                                alt={`Foto ${idx + 1}`}
                                className="w-full h-32 object-cover rounded-lg"
                              />
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Note finali */}
      <div className="card mt-6">
        <label className="flex items-center gap-2 mb-3 font-semibold">
          <FileText size={20} />
          Note Aggiuntive
        </label>
        <textarea
          className="w-full p-3 border-2 border-gray-300 rounded-lg mb-3"
          rows="4"
          placeholder="Problemi riscontrati, segnalazioni, ecc..."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          disabled={checklist.completed}
        />
        {!checklist.completed && (
          <button
            onClick={handleSaveNotes}
            className="btn btn-outline"
          >
            <Save size={20} />
            Salva Note
          </button>
        )}
      </div>

      {/* Pulsante completamento */}
      {!checklist.completed && (
        <div className="card mt-6 bg-secondary text-white">
          <button
            onClick={handleCompleteChecklist}
            className="btn w-full bg-white text-secondary hover:bg-gray-100"
            disabled={saving}
          >
            {saving ? (
              <>
                <div className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }}></div>
                Salvataggio...
              </>
            ) : (
              <>
                <CheckCircle2 size={24} />
                Completa Checklist
              </>
            )}
          </button>
          <p className="text-center text-sm mt-3 opacity-90">
            Assicurati di aver completato tutte le task obbligatorie
          </p>
        </div>
      )}
    </div>
  );
};

export default ChecklistPage;



