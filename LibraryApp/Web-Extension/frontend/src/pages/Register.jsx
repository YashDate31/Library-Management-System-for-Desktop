import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { UserPlus } from 'lucide-react';

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

const CustomSelect = ({ label, value, onChange, children, required = true }) => (
  <div className="space-y-1.5">
    <label className="block text-sm font-medium text-slate-700">{label}</label>
    <select
      value={value}
      onChange={onChange}
      required={required}
      className="w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-blue-600 focus:ring-1 focus:ring-blue-600 outline-none transition-all bg-white text-slate-800"
    >
      {children}
    </select>
  </div>
);

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    enrollment_no: '',
    name: '',
    year: '',
    department: 'Computer',
    phone: '',
    email: ''
  });
  const [photo, setPhoto] = useState(null);

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const onField = (key) => (e) => {
    setForm((prev) => ({ ...prev, [key]: e.target.value }));
  };

  const handlePhoto = (e) => {
    const file = e.target.files?.[0] || null;
    if (!file) {
      setPhoto(null);
      return;
    }

    // 50KB limit (client-side). Server also enforces.
    if (file.size > 50 * 1024) {
      setError('Photo too large. Max size is 50KB.');
      e.target.value = '';
      setPhoto(null);
      return;
    }

    const ext = (file.name.split('.').pop() || '').toLowerCase();
    if (!['jpg', 'jpeg', 'png'].includes(ext)) {
      setError('Photo must be JPG or PNG.');
      e.target.value = '';
      setPhoto(null);
      return;
    }

    setError('');
    setPhoto(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const fd = new FormData();
      fd.append('enrollment_no', form.enrollment_no);
      fd.append('name', form.name);
      fd.append('year', form.year);
      fd.append('department', form.department);
      fd.append('phone', form.phone);
      fd.append('email', form.email);
      if (photo) fd.append('photo', photo);

      const { data } = await axios.post('/api/public/register', fd);

      if (data.status === 'success') {
        setSuccess(data.message || 'Registration request submitted.');
        // Small delay so user sees success message
        setTimeout(() => navigate('/login'), 1200);
      } else {
        setError(data.message || 'Registration failed');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-blue-50/50 text-slate-800">
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-200/30 rounded-full blur-3xl"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-200/30 rounded-full blur-3xl"></div>

      <div className="w-full max-w-[560px] bg-white p-8 md:p-10 rounded-[2rem] shadow-xl shadow-blue-900/5 relative z-10 border border-white">
        <div className="flex flex-col items-center mb-8 text-center">
          <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mb-3">
            <UserPlus size={24} />
          </div>
          <h2 className="text-2xl font-bold text-slate-900 mb-1">New Student Registration</h2>
          <p className="text-sm text-slate-500 font-medium">Submit your details. Librarian will approve/reject.</p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-xl mb-6 text-sm font-medium border border-red-100 flex items-center justify-center">
            {error}
          </div>
        )}

        {success && (
          <div className="bg-green-50 text-green-700 p-3 rounded-xl mb-6 text-sm font-medium border border-green-100 flex items-center justify-center">
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <CustomInput
              label="Enrollment Number"
              type="text"
              value={form.enrollment_no}
              onChange={onField('enrollment_no')}
              placeholder="e.g. 210101"
            />
            <CustomInput
              label="Full Name"
              type="text"
              value={form.name}
              onChange={onField('name')}
              placeholder="Your name"
            />

            <CustomSelect label="Year" value={form.year} onChange={onField('year')}>
              <option value="" disabled>
                Select year
              </option>
              <option value="1st">1st Year</option>
              <option value="2nd">2nd Year</option>
              <option value="3rd">3rd Year</option>
            </CustomSelect>

            <CustomSelect label="Branch / Department" value={form.department} onChange={onField('department')}>
              <option value="Computer">Computer</option>
              <option value="Mechanical">Mechanical</option>
              <option value="Civil">Civil</option>
              <option value="Electrical">Electrical</option>
              <option value="Electronics">Electronics</option>
              <option value="IT">IT</option>
              <option value="Other">Other</option>
            </CustomSelect>

            <CustomInput
              label="Mobile"
              type="text"
              value={form.phone}
              onChange={onField('phone')}
              placeholder="e.g. 9876543210"
            />
            <CustomInput
              label="Email"
              type="email"
              value={form.email}
              onChange={onField('email')}
              placeholder="you@example.com"
            />
          </div>

          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-slate-700">Photo (optional, max 50KB)</label>
            <input
              type="file"
              accept="image/png,image/jpeg"
              onChange={handlePhoto}
              className="w-full px-4 py-3 rounded-xl border border-slate-300 bg-white text-slate-700"
            />
            <p className="text-xs text-slate-400">Allowed: JPG, PNG. Keep it small for fast approval workflow.</p>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-blue-600/20 active:scale-[0.98] disabled:opacity-70 disabled:scale-100 mt-2"
          >
            {loading ? 'Submitting...' : 'Submit Registration Request'}
          </button>

          <div className="text-center mt-4">
            <Link to="/login" className="text-sm text-blue-600 font-medium hover:underline">
              Back to Login
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
