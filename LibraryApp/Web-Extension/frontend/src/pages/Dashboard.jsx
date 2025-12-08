import { useState, useEffect } from 'react';
import axios from 'axios';
import { Book, Clock, AlertCircle, CheckCircle } from 'lucide-react';

export default function Dashboard({ user }) {
  const [data, setData] = useState({ borrows: [], history: [], notices: [] });
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

  if (loading) return <div className="p-10 text-center">Loading dashboard...</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-12 gap-6 pb-10">
      
      {/* Welcome Banner */}
      <div className="md:col-span-12 relative overflow-hidden rounded-3xl bg-gradient-to-r from-primary to-primary-dark text-white p-8 shadow-xl shadow-primary/20">
        <div className="absolute top-0 right-0 p-10 opacity-10 transform translate-x-10 -translate-y-10">
          <Book size={200} />
        </div>
        <div className="relative z-10">
          <h1 className="text-3xl font-bold mb-2">Hello, {user.name.split(' ')[0]}!</h1>
          <p className="opacity-90">Welcome to your personalized library dashboard.</p>
          
          <div className="flex gap-4 mt-6">
            <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-2">
              <Book size={16} /> {data.borrows.length} Active Loans
            </div>
            <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-2">
              <Clock size={16} /> {user.year}
            </div>
          </div>
        </div>
      </div>

      {/* Profile Card */}
      <div className="md:col-span-4 glass rounded-3xl p-6 flex flex-col gap-4">
        <h3 className="text-lg font-bold text-slate-800 border-b border-slate-100 pb-2">Student Profile</h3>
        <ProfileRow label="Name" value={user.name} />
        <ProfileRow label="Enrollment" value={user.enrollment_no} />
        <ProfileRow label="Department" value={user.department} />
        <ProfileRow label="Year" value={user.year} />
      </div>

      {/* Current Borrows */}
      <div className="md:col-span-8 glass rounded-3xl p-6">
        <h3 className="text-lg font-bold text-slate-800 border-b border-slate-100 pb-4 mb-4 flex justify-between items-center">
          Current Loans
          <span className="text-xs bg-indigo-50 text-indigo-600 px-3 py-1 rounded-full">{data.borrows.length} Books</span>
        </h3>
        
        {data.borrows.length === 0 ? (
          <p className="text-slate-400 text-center py-8">No active loans.</p>
        ) : (
          <div className="flex flex-col gap-3">
            {data.borrows.map((book, i) => (
              <div key={i} className="flex items-center justify-between p-4 bg-white/50 rounded-xl border border-white hover:shadow-md transition">
                <div>
                  <h4 className="font-semibold text-slate-800">{book.title}</h4>
                  <p className="text-sm text-slate-500">{book.author}</p>
                </div>
                <div className="text-right">
                  <StatusBadge status={book.status} days={book.days_left} />
                  <p className="text-xs text-slate-400 mt-1">Due: {book.due_date}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Reading History */}
      <div className="md:col-span-8 glass rounded-3xl p-6">
        <h3 className="text-lg font-bold text-slate-800 mb-6">Reading Journey</h3>
        <div className="relative pl-4 ml-2 border-l-2 border-slate-200 space-y-8">
          {data.history.map((book, i) => (
            <div key={i} className="relative pl-6">
              <div className="absolute -left-[21px] top-1 w-3 h-3 bg-white border-2 border-primary rounded-full ring-4 ring-slate-50"></div>
              <div className="bg-white p-4 rounded-xl border border-slate-100 shadow-sm hover:shadow-md transition transform hover:translate-x-1">
                <span className="text-xs font-bold text-primary uppercase tracking-wider">{book.return_date}</span>
                <h4 className="font-semibold text-slate-800 mt-1">{book.title}</h4>
                <p className="text-xs text-slate-500">by {book.author}</p>
              </div>
            </div>
          ))}
          {data.history.length === 0 && <p className="text-slate-400 pl-6">No history available.</p>}
        </div>
      </div>

      {/* Notices */}
      <div className="md:col-span-4 glass rounded-3xl p-6">
        <h3 className="text-lg font-bold text-slate-800 mb-4">Notice Board</h3>
        <div className="space-y-4">
          {data.notices.map((notice, i) => (
            <div key={i} className="p-4 bg-yellow-50/50 rounded-xl border border-yellow-100">
              <div className="flex items-center gap-2 mb-2">
                <AlertCircle size={16} className="text-yellow-600" />
                <span className="text-xs font-bold text-yellow-700">{notice.date}</span>
              </div>
              <h4 className="font-semibold text-slate-800 text-sm">{notice.title}</h4>
              <p className="text-xs text-slate-600 mt-1 leading-relaxed">{notice.msg}</p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}

function ProfileRow({ label, value }) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-slate-50 last:border-0">
      <span className="text-slate-500 text-sm">{label}</span>
      <span className="font-semibold text-slate-800 text-right">{value}</span>
    </div>
  );
}

function StatusBadge({ status, days }) {
  if (status === 'overdue') {
    return <span className="inline-flex items-center gap-1 px-2 py-1 bg-red-100 text-red-600 rounded-full text-xs font-bold">Overdue ({days}d)</span>;
  }
  if (status === 'due_soon') {
    return <span className="inline-flex items-center gap-1 px-2 py-1 bg-orange-100 text-orange-600 rounded-full text-xs font-bold">Due in {days}d</span>;
  }
  return <span className="inline-flex items-center gap-1 px-2 py-1 bg-emerald-100 text-emerald-600 rounded-full text-xs font-bold">Active ({days}d left)</span>;
}
