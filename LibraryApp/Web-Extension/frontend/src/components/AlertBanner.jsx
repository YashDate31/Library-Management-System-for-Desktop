import { useState, useEffect } from 'react';
import { AlertCircle, ChevronRight, X } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import axios from 'axios';

export default function AlertBanner() {
  const [alert, setAlert] = useState(null);
  const [visible, setVisible] = useState(true);
  const location = useLocation();
  const isDashboard = location.pathname === '/';

  useEffect(() => {
    const checkAlerts = async () => {
      try {
        const { data } = await axios.get('/api/alerts');
        if (data.has_alert) {
          setAlert(data);
        }
      } catch (e) {
        // Silent fail for alerts
        console.error("Alert check failed", e);
      }
    };

    checkAlerts();
    // Optional: Poll every 5 minutes if needed, but on-mount is sufficient for MVP
  }, []);

  // Hide on Dashboard (avoid double alert) or if dismissed
  if (!alert || !visible || isDashboard) return null;

  return (
    <div className="bg-red-600 text-white px-4 py-3 shadow-md relative z-50 animate-slide-in">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        
        <div className="flex items-center gap-3">
          <div className="bg-white/20 p-1.5 rounded-full shrink-0 animate-pulse">
            <AlertCircle size={20} className="text-white" />
          </div>
          <div className="font-medium text-sm md:text-base">
            <span className="font-bold">Attention Needed:</span> You have {alert.count} overdue book{alert.count > 1 ? 's' : ''}. 
            <span className="opacity-90 hidden sm:inline"> Estimated fine: ₹{alert.fine_estimate}.</span>
          </div>
        </div>

        <div className="flex items-center gap-4 shrink-0">
          <Link 
            to="/" 
            className="text-white text-sm font-semibold hover:underline flex items-center gap-1 group bg-white/10 px-3 py-1.5 rounded-lg hover:bg-white/20 transition"
          >
            Details <ChevronRight size={16} className="group-hover:translate-x-0.5 transition-transform" />
          </Link>
          <button 
            onClick={() => setVisible(false)} 
            className="text-white/70 hover:text-white p-1 hover:bg-red-700 rounded-md transition"
          >
            <X size={18} />
          </button>
        </div>

      </div>
    </div>
  );
}
