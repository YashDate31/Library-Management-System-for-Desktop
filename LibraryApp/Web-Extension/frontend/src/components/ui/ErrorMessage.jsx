import { AlertTriangle, RefreshCw } from 'lucide-react';

export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center rounded-xl bg-red-50 border border-red-100 animate-fade-in">
      <div className="w-12 h-12 bg-red-100 text-red-500 rounded-full flex items-center justify-center mb-4">
        <AlertTriangle size={24} />
      </div>
      <h3 className="text-lg font-bold text-red-900 mb-1">Something went wrong</h3>
      <p className="text-red-600 mb-6 max-w-sm">{message || 'An unexpected error occurred. Please try again.'}</p>
      
      {onRetry && (
        <button 
          onClick={onRetry}
          className="flex items-center gap-2 px-4 py-2 bg-white border border-red-200 text-red-700 font-medium rounded-lg hover:bg-red-50 transition-colors shadow-sm"
        >
          <RefreshCw size={16} />
          Try Again
        </button>
      )}
    </div>
  );
}
