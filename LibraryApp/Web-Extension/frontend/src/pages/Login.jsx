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
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-background text-text-primary">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-secondary/10 to-purple-500/10 animate-gradient-xy"></div>
      
      <div className="glass w-full max-w-md p-8 rounded-2xl relative z-10 border border-border bg-surface/50 backdrop-blur-xl">
        <div className="flex justify-center mb-6">
           <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-primary/20">
             <BookOpen size={40} />
           </div>
        </div>

        <h2 className="text-2xl font-bold text-center mb-2 text-text-primary">Welcome Back</h2>
        <p className="text-center text-text-secondary mb-8">Access your digital library portal</p>

        {error && (
          <div className="bg-danger/10 text-danger p-3 rounded-lg mb-4 text-sm border border-danger/20">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label className="block text-sm font-semibold text-text-primary mb-2">Enrollment Number</label>
            <input 
              type="text" 
              value={enrollment}
              onChange={(e) => setEnrollment(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition bg-background text-text-primary placeholder:text-text-secondary"
              placeholder="e.g. 210101"
              required
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full py-3 bg-primary hover:bg-blue-600 text-white font-bold rounded-xl transition shadow-lg shadow-primary/20 disabled:opacity-70"
          >
            {loading ? 'Accessing...' : 'Enter Library'}
          </button>
        </form>
      </div>
    </div>
  );
}
