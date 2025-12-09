import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { BookOpen } from 'lucide-react';

// Custom Input Component to match the design (Green focus)
const CustomInput = ({ label, type, value, onChange, placeholder, required = true }) => (
  <div className="space-y-1.5">
      <label className="block text-sm font-medium text-slate-700">{label}</label>
      <input 
        type={type} 
        value={value}
        onChange={onChange}
        className="w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-blue-600 focus:ring-1 focus:ring-blue-600 outline-none transition-all bg-white text-slate-800 placeholder:text-slate-400"
        placeholder={placeholder}
        required={required}
      />
  </div>
);

export default function Login({ setUser }) {
  const [enrollment, setEnrollment] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  // New States for Password Change
  const [requireChange, setRequireChange] = useState(false);
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const { data } = await axios.post('/api/login', { 
        enrollment_no: enrollment,
        password: password || enrollment 
      });
      
      if (data.status === 'success') {
        // Updated Logic: Always allow login, dashboard will show alert if password change is needed
        setUser(data.user);
        // We ignore data.require_change for blocking now
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    // Logic preserved for Settings page or future use, but not for login blocking
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-blue-50/50 text-slate-800">
      {/* Background blobs for subtle effect */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-200/30 rounded-full blur-3xl"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-200/30 rounded-full blur-3xl"></div>
      
      <div className="w-full max-w-[480px] bg-white p-8 md:p-10 rounded-[2rem] shadow-xl shadow-blue-900/5 relative z-10 border border-white">
        <div className="flex flex-col items-center mb-10">
            {/* Official Header Section */}
            <div className="flex flex-col items-center gap-4 mb-4 text-center">
                <img src="/logo.png" alt="College Logo" className="w-20 h-20 object-contain drop-shadow-sm" />
                <div className="space-y-1">
                  <h1 className="text-xl font-bold text-slate-900 leading-tight">Government Polytechnic, Awasari (Kh.)</h1>
                  <h2 className="text-lg font-bold text-slate-700 font-serif">शासकीय तंत्रनिकेतन, अवसरी (खु.)</h2>
                </div>
            </div>

            {/* Divider */}
            <div className="w-16 h-1 bg-blue-100 rounded-full mb-8"></div>
           
           <h2 className="text-2xl font-bold text-slate-900 mb-2">
             {requireChange ? "Set New Password" : "Welcome Back"}
           </h2>
           <p className="text-sm text-slate-500 font-medium">
             {requireChange ? "Secure your account by verifying your details" : "Access your digital library portal"}
           </p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-xl mb-6 text-sm font-medium border border-red-100 flex items-center justify-center">
            {error}
          </div>
        )}

        {!requireChange ? (
          <form onSubmit={handleSubmit} className="space-y-5">
            <CustomInput 
              label="Enrollment Number"
              type="text"
              value={enrollment}
              onChange={(e) => setEnrollment(e.target.value)}
              placeholder="e.g. 210101"
            />
            
            <CustomInput 
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
            />

            <button 
              type="submit" 
              disabled={loading}
              className="w-full py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-blue-600/20 active:scale-[0.98] disabled:opacity-70 disabled:scale-100 mt-2"
            >
              {loading ? 'Verifying...' : 'Login'}
            </button>
            
            <p className="text-xs text-center text-slate-400 mt-4">
              First time? Use your enrollment number as password.
            </p>
          </form>
        ) : (
          <form onSubmit={handlePasswordChange} className="space-y-5 animate-fade-in">
             <CustomInput 
              label="New Password"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Enter new password"
            />
             <CustomInput 
              label="Confirm Password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm new password"
            />

            <button 
              type="submit" 
              disabled={loading}
              className="w-full py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-emerald-600/20 active:scale-[0.98] disabled:opacity-70 disabled:scale-100 mt-2"
            >
              {loading ? 'Updating...' : 'Set Password & Login'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
