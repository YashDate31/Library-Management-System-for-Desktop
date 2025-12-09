import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { BookOpen } from 'lucide-react';

export default function Login({ setUser }) {
  const [enrollment, setEnrollment] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const { data } = await axios.post('/api/login', { enrollment_no: enrollment });
      if (data.status === 'success') {
        setUser(data.user);
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-blue-50/50 text-slate-800">
      {/* Background blobs for subtle effect */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-200/30 rounded-full blur-3xl"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-200/30 rounded-full blur-3xl"></div>
      
      <div className="w-full max-w-sm bg-white p-8 rounded-[2rem] shadow-xl shadow-blue-900/5 relative z-10 border border-white">
        <div className="flex flex-col items-center mb-8">
            {/* Logo Section */}
            <div className="flex flex-col items-center gap-2 mb-6">
                <img src="/logo.png" alt="College Logo" className="w-12 h-12 object-contain" />
                <h1 className="text-sm font-bold text-slate-500 uppercase tracking-widest">GPA's Library</h1>
            </div>

            {/* Icon */}
           <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-blue-500/30 mb-6 transform rotate-3">
             <BookOpen size={32} strokeWidth={2.5} />
           </div>
           
           <h2 className="text-2xl font-bold text-slate-900 mb-2">Welcome Back</h2>
           <p className="text-sm text-slate-500 font-medium">Access your digital library portal</p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-xl mb-6 text-sm font-medium border border-red-100 flex items-center justify-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="block text-xs font-bold text-slate-700 ml-1">Enrollment Number</label>
            <input 
              type="text" 
              value={enrollment}
              onChange={(e) => setEnrollment(e.target.value)}
              className="w-full px-5 py-3.5 rounded-xl border border-slate-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all bg-slate-50 text-slate-900 placeholder:text-slate-400 font-medium text-sm"
              placeholder="e.g. 210101"
              required
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-blue-600/20 active:scale-[0.98] disabled:opacity-70 disabled:scale-100"
          >
            {loading ? 'Accessing...' : 'Enter Library'}
          </button>
        </form>
      </div>
    </div>
  );
}
