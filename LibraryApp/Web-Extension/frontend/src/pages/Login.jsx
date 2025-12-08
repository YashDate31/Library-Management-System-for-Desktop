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
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/20 via-purple-500/20 to-pink-500/20 animate-gradient-xy"></div>
      
      <div className="glass w-full max-w-md p-8 rounded-2xl relative z-10">
        <div className="flex justify-center mb-6">
          <div className="w-20 h-20 bg-gradient-to-tr from-primary to-accent rounded-2xl flex items-center justify-center text-white shadow-lg shadow-indigo-500/30">
            <BookOpen size={40} />
          </div>
        </div>

        <h2 className="text-2xl font-bold text-center mb-2">Welcome Back</h2>
        <p className="text-center text-slate-500 mb-8">Access your digital library portal</p>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm border border-red-100">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label className="block text-sm font-semibold text-slate-700 mb-2">Enrollment Number</label>
            <input 
              type="text" 
              value={enrollment}
              onChange={(e) => setEnrollment(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition bg-white/50"
              placeholder="e.g. 210101"
              required
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full py-3 bg-primary hover:bg-primary-dark text-white font-bold rounded-xl transition shadow-lg shadow-indigo-500/20 disabled:opacity-70"
          >
            {loading ? 'Accessing...' : 'Enter Library'}
          </button>
        </form>
      </div>
    </div>
  );
}
