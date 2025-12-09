import { createContext, useContext, useState, useEffect } from 'react';
import { X, CheckCircle, AlertCircle, Info } from 'lucide-react';

const ToastContext = createContext();

export function useToast() {
  return useContext(ToastContext);
}

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const addToast = (message, type = 'info', duration = 3000) => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, message, type }]);

    if (duration) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }
  };

  const removeToast = (id) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  };

  const success = (msg) => addToast(msg, 'success');
  const error = (msg) => addToast(msg, 'error');
  const info = (msg) => addToast(msg, 'info');

  return (
    <ToastContext.Provider value={{ success, error, info, addToast }}>
      {children}
      
      {/* Toast Container */}
      <div className="fixed top-4 right-4 z-[100] flex flex-col gap-2 pointer-events-none">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`
              pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg border toast-enter
              ${toast.type === 'success' ? 'bg-white border-green-100 text-green-800' : ''}
              ${toast.type === 'error' ? 'bg-white border-red-100 text-red-800' : ''}
              ${toast.type === 'info' ? 'bg-white border-blue-100 text-slate-800' : ''}
            `}
          >
            {toast.type === 'success' && <CheckCircle size={18} className="text-green-500" />}
            {toast.type === 'error' && <AlertCircle size={18} className="text-red-500" />}
            {toast.type === 'info' && <Info size={18} className="text-blue-500" />}
            
            <span className="text-sm font-medium">{toast.message}</span>
            
            <button 
              onClick={() => removeToast(toast.id)}
              className="ml-2 text-slate-400 hover:text-slate-600"
            >
              <X size={14} />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}
