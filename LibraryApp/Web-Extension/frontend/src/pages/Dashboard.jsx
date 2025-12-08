import { useState, useEffect } from 'react';
import axios from 'axios';
import { Book, Clock, AlertCircle, CheckCircle, Bell, FileText } from 'lucide-react';

export default function Dashboard({ user }) {
  const [data, setData] = useState({ 
    borrows: [], 
    history: [], 
    notices: [], 
    notifications: [],
    recent_requests: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const { data } = await axios.get('/api/dashboard');
      setData(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-10 text-center animate-pulse">Loading your dashboard...</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-12 gap-6 pb-10">
      
      {/* Notifications Banner */}
      {data.notifications.length > 0 && (
        <div className="md:col-span-12 space-y-2">
          {data.notifications.map((notif, i) => (
            <div key={i} className={`p-4 rounded-xl border flex items-center gap-3 ${
              notif.type === 'danger' ? 'bg-red-50 border-red-100 text-red-700' : 'bg-orange-50 border-orange-100 text-orange-700'
            }`}>
              <Bell size={18} />
              <span className="font-semibold">{notif.msg}</span>
            </div>
          ))}
        </div>
      )}

      {/* Welcome Area */}
      <div className="md:col-span-8 relative overflow-hidden rounded-3xl bg-gradient-to-r from-primary to-primary-dark text-white p-8 shadow-xl shadow-primary/20">
        <div className="absolute top-0 right-0 p-10 opacity-10 transform translate-x-10 -translate-y-10">
          <Book size={200} />
        </div>
        <div className="relative z-10">
          <h1 className="text-3xl font-bold mb-2">Hello, {user.name.split(' ')[0]}!</h1>
          <p className="opacity-90">Are you ready to learn something new today?</p>
          
          <div className="flex flex-wrap gap-4 mt-8">
            <StatsChip icon={<Book size={16} />} label={`${data.borrows.length} Active Loans`} />
            <StatsChip icon={<Clock size={16} />} label={user.year} />
          </div>
        </div>
      </div>

      {/* Profile / Quick Actions */}
      <div className="md:col-span-4 glass rounded-3xl p-6 flex flex-col justify-between">
        <div>
           <h3 className="text-lg font-bold text-slate-800 mb-4">Student Profile</h3>
           <ProfileRow label="Enrollment" value={user.enrollment_no} />
           <ProfileRow label="Department" value={user.department} />
        </div>
        <button className="w-full mt-4 py-2 border border-slate-200 rounded-xl text-slate-600 font-medium hover:bg-slate-50 transition text-sm">
          Request Profile Update
        </button>
      </div>

      {/* Active Loans */}
      <div className="md:col-span-8 glass rounded-3xl p-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-bold text-slate-800">Current Loans</h3>
        </div>
        
        {data.borrows.length === 0 ? (
          <div className="text-center py-10 bg-slate-50/50 rounded-2xl border border-dashed border-slate-200">
            <p className="text-slate-400">No books currently borrowed.</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {data.borrows.map((book, i) => (
              <LoanCard key={i} book={book} />
            ))}
          </div>
        )}
      </div>

      {/* Side Panel: Notices & Requests */}
      <div className="md:col-span-4 space-y-6">
        {/* Notices */}
        <div className="glass rounded-3xl p-6">
          <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
            <AlertCircle size={18} className="text-accent" /> Notices
          </h3>
          <div className="space-y-4">
            {data.notices.map((notice, i) => (
              <div key={i} className="pb-3 border-b border-slate-50 last:border-0 last:pb-0">
                <p className="text-xs font-bold text-accent mb-0.5">{notice.date}</p>
                <p className="text-sm font-medium text-slate-700">{notice.title}</p>
                <p className="text-xs text-slate-500 mt-1 line-clamp-2">{notice.content}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Requests */}
        <div className="glass rounded-3xl p-6">
          <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
            <FileText size={18} className="text-secondary" /> My Requests
          </h3>
           {data.recent_requests.length === 0 ? (
             <p className="text-xs text-slate-400">No active requests.</p>
           ) : (
             <div className="space-y-3">
               {data.recent_requests.map((req, i) => (
                 <div key={i} className="flex justify-between items-center text-sm">
                   <span className="text-slate-600 capitalize">{req.request_type.replace('_', ' ')}</span>
                   <span className={`px-2 py-0.5 rounded-full text-xs font-bold capitalize ${
                     req.status === 'pending' ? 'bg-yellow-100 text-yellow-700' : 
                     req.status === 'approved' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                   }`}>{req.status}</span>
                 </div>
               ))}
             </div>
           )}
        </div>
      </div>

    </div>
  );
}

// Sub-components
function StatsChip({ icon, label }) {
  return (
    <div className="bg-white/20 backdrop-blur-md px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-2 border border-white/10">
      {icon} {label}
    </div>
  );
}

function ProfileRow({ label, value }) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-slate-50 last:border-0">
      <span className="text-slate-400 text-sm">{label}</span>
      <span className="font-semibold text-slate-700">{value}</span>
    </div>
  );
}

function LoanCard({ book }) {
  const statusColors = {
    safe: 'bg-emerald-50 text-emerald-600 border-emerald-100',
    warning: 'bg-amber-50 text-amber-600 border-amber-100',
    overdue: 'bg-red-50 text-red-600 border-red-100'
  };

  return (
    <div className="flex items-center justify-between p-4 bg-white rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition">
      <div className="flex items-center gap-4">
        <div className="w-12 h-16 bg-slate-100 rounded-lg flex items-center justify-center text-slate-300">
          <Book size={24} />
        </div>
        <div>
          <h4 className="font-bold text-slate-800">{book.title}</h4>
          <p className="text-sm text-slate-500">{book.author}</p>
        </div>
      </div>
      <div className={`text-right px-4 py-2 rounded-xl border ${statusColors[book.status] || statusColors.safe}`}>
        <p className="text-xs font-bold uppercase tracking-wider">{book.status}</p>
        <p className="text-sm font-bold">{book.days_msg}</p>
      </div>
    </div>
  );
}
