import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Camera, Mail, GraduationCap, Building2, Calendar, Book, Clock, RefreshCw, Key, ShieldCheck, CheckCircle2, Shield } from 'lucide-react';
import { SkeletonCard } from '../components/ui/Skeleton';
import ErrorMessage from '../components/ui/ErrorMessage';
import { motion } from 'framer-motion';

export default function Profile({ user }) {
  const [policies, setPolicies] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [profilePhoto, setProfilePhoto] = useState(null);
  const [uploadingPhoto, setUploadingPhoto] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    const fetchPolicies = async () => {
      try {
        const { data } = await axios.get('/api/user-policies');
        setPolicies(data.policies);
      } catch (e) {
        console.error("Failed to fetch policies", e);
        setError("Could not load details");
      } finally {
        setLoading(false);
      }
    };
    
    // Load saved profile photo
    const savedPhoto = localStorage.getItem('profilePhoto');
    if (savedPhoto) setProfilePhoto(savedPhoto);
    
    fetchPolicies();
  }, []);

  const handlePhotoUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      alert('File size must be less than 5MB');
      return;
    }

    if (!file.type.startsWith('image/')) {
      alert('Please select an image file');
      return;
    }

    setUploadingPhoto(true);
    const reader = new FileReader();
    reader.onload = (event) => {
      const photoData = event.target.result;
      setProfilePhoto(photoData);
      localStorage.setItem('profilePhoto', photoData);
      setUploadingPhoto(false);
    };
    reader.readAsDataURL(file);
  };

  const profile = {
    name: user?.name || "Student",
    id: user?.enrollment_no || "N/A",
    department: user?.department || "General",
    year: user?.year ? `${user.year}` : "N/A",
    email: user?.email || "N/A",
  };

  const InfoRow = ({ icon: Icon, label, value, loading }) => (
    <div className="flex items-center gap-4 p-4 rounded-xl bg-slate-50 hover:bg-slate-100 transition-colors border border-slate-100">
        <div className="bg-white p-2.5 rounded-full shadow-sm text-slate-500 shrink-0">
            <Icon size={20} />
        </div>
        <div className="flex-1 min-w-0">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-0.5">{label}</p>
            <p className="text-slate-900 font-semibold truncate">
                {loading ? <div className="h-5 w-24 bg-slate-200 rounded animate-pulse"/> : value}
            </p>
        </div>
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 pb-20 font-sans">
      
      {/* Page Title */}
      <div className="mb-8">
        <h1 className="text-3xl font-black text-slate-900 tracking-tight mb-1">Student Profile</h1>
        <p className="text-slate-500">Manage your account settings and preferences.</p>
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="grid grid-cols-1 lg:grid-cols-3 gap-8"
      >
        
        {/* Left Column: Digital ID Card */}
        <div className="space-y-6">
          
          {/* Main ID Card */}
          <div className="relative group perspective-1000">
             <div className="absolute inset-0 bg-blue-600 rounded-3xl blur-xl opacity-20 group-hover:opacity-30 transition-opacity duration-500"></div>
             <div className="relative bg-gradient-to-br from-blue-600 to-indigo-700 rounded-3xl p-8 text-white shadow-2xl overflow-hidden flex flex-col items-center text-center">
                
                {/* Decorative Pattern */}
                <div className="absolute top-0 left-0 w-full h-full opacity-10">
                    <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                        <defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="white" strokeWidth="1"/></pattern></defs>
                        <rect width="100%" height="100%" fill="url(#grid)" />
                    </svg>
                </div>

                {/* Avatar */}
                <div className="relative mb-4 group-hover:scale-105 transition-transform duration-300">
                    <div className="w-28 h-28 rounded-full border-4 border-white/30 shadow-lg overflow-hidden relative z-10 bg-white">
                        <img
                            src={profilePhoto || `https://ui-avatars.com/api/?name=${encodeURIComponent(profile.name)}&background=random&color=fff&size=256`}
                            alt={profile.name}
                            className="w-full h-full object-cover"
                        />
                        <button
                            onClick={() => fileInputRef.current?.click()}
                            disabled={uploadingPhoto}
                            className="absolute inset-0 bg-black/40 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center cursor-pointer"
                        >
                            <Camera className="w-8 h-8 text-white drop-shadow-md" />
                        </button>
                         <input
                            ref={fileInputRef}
                            type="file"
                            accept="image/*"
                            onChange={handlePhotoUpload}
                            className="hidden"
                        />
                    </div>
                </div>

                {/* Name & ID */}
                <div className="relative z-10">
                    <h2 className="text-2xl font-bold mb-1">{profile.name}</h2>
                    <p className="text-blue-200 font-mono tracking-wider text-sm opacity-90">{profile.id}</p>
                </div>

                {/* Department Badge */}
                <div className="relative z-10 mt-6 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
                    <span className="text-xs font-bold tracking-wide uppercase">{profile.department} • Year {profile.year}</span>
                </div>

             </div>
          </div>
          
          {/* Status Pills */}
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
             <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4">Current Status</h3>
             <div className="space-y-3">
               <div className="flex items-center gap-3 bg-emerald-50 text-emerald-700 px-4 py-3 rounded-xl border border-emerald-100">
                 <div className="bg-emerald-100 p-1.5 rounded-full"><CheckCircle2 size={16} /></div>
                 <span className="font-semibold text-sm">Active Membership</span>
               </div>
               <div className="flex items-center gap-3 bg-blue-50 text-blue-700 px-4 py-3 rounded-xl border border-blue-100">
                 <div className="bg-blue-100 p-1.5 rounded-full"><ShieldCheck size={16} /></div>
                 <span className="font-semibold text-sm">No Outstanding Fines</span>
               </div>
             </div>
          </div>
          
        </div>
        
        {/* Right Column: Info Grids */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Academic Info */}
          <section>
            <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                <GraduationCap className="text-blue-500" /> Academic Information
            </h3>
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                <InfoRow icon={Building2} label="Department" value={profile.department} />
                <InfoRow icon={Calendar} label="Current Year" value={profile.year} />
                <InfoRow icon={Mail} label="Email Address" value={profile.email} />
                <InfoRow icon={Shield} label="Student ID" value={profile.id} />
            </div>
          </section>
          
          {/* Library Privileges */}
          <section>
            <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                <Book className="text-purple-500" /> Borrowing Privileges
            </h3>
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                <InfoRow icon={Book} label="Max Books" value={`${policies?.max_books || 0} Books`} loading={loading} />
                <InfoRow icon={Clock} label="Loan Duration" value={`${policies?.loan_duration || 0} Days`} loading={loading} />
                <InfoRow icon={RefreshCw} label="Renewals" value={`${policies?.renewal_limit || 0} Times`} loading={loading} />
            </div>
          </section>

          {/* Account Settings */}
          <section>
             <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                <Key className="text-slate-500" /> Security
            </h3>
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex flex-col md:flex-row items-center justify-between gap-4">
                 <div className="flex items-center gap-4">
                     <div className="bg-orange-50 p-3 rounded-full text-orange-600">
                         <Key size={24} />
                     </div>
                     <div>
                         <h4 className="font-bold text-slate-900">Password</h4>
                         <p className="text-sm text-slate-500">
                             Last changed: {loading ? 'Loading...' : policies?.password_last_changed || 'Unknown'}
                         </p>
                     </div>
                 </div>
                 <Link 
                   to="/settings" 
                   className="px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-xl transition-all shadow-lg shadow-slate-200"
                 >
                   Change Password
                 </Link>
            </div>
          </section>
          
        </div>
      </motion.div>
    </div>
  );
}
