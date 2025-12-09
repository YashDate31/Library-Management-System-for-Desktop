import React from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';
import { Link } from 'react-router-dom';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Uncaught error:", error, errorInfo);
    // Here you would log to an error reporting service
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-slate-50 p-6 font-sans">
          <div className="max-w-md w-full bg-white rounded-2xl shadow-xl border border-slate-100 p-8 text-center animate-fade-in">
            <div className="w-16 h-16 bg-red-100 text-red-500 rounded-full flex items-center justify-center mx-auto mb-6">
              <AlertTriangle size={32} />
            </div>
            
            <h1 className="text-2xl font-bold text-slate-900 mb-2">Something went wrong</h1>
            <p className="text-slate-500 mb-8">
              We encountered an unexpected error. Please try reloading the page.
            </p>

            <div className="flex flex-col gap-3">
              <button 
                onClick={this.handleRetry}
                className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-brand-blue hover:bg-blue-600 text-white font-bold rounded-xl transition-colors shadow-lg shadow-blue-500/20"
              >
                <RefreshCw size={18} />
                Reload Application
              </button>
              
              <a 
                href="/"
                className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl transition-colors"
                onClick={(e) => {
                   e.preventDefault();
                   window.location.href = '/';
                }}
              >
                <Home size={18} />
                Go to Dashboard
              </a>
            </div>

            {this.state.error && (
               <div className="mt-8 p-4 bg-slate-50 rounded-lg border border-slate-200 text-left overflow-auto max-h-40">
                 <p className="text-xs font-mono text-slate-600 break-all">
                   {this.state.error.toString()}
                 </p>
               </div>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
