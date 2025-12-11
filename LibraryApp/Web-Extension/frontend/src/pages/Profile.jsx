import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Camera } from 'lucide-react';
import Skeleton from '../components/ui/Skeleton';
import ErrorMessage from '../components/ui/ErrorMessage';
import ImageWithSkeleton from '../components/ui/ImageWithSkeleton';

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
    
    // Load saved profile photo from localStorage
    const savedPhoto = localStorage.getItem('profilePhoto');
    if (savedPhoto) {
      setProfilePhoto(savedPhoto);
    }
    
    fetchPolicies();
  }, []);

  const handlePhotoUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('File size must be less than 5MB');
      return;
    }

    // Check file type
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
    reader.onerror = () => {
      alert('Failed to read file');
      setUploadingPhoto(false);
    };
    reader.readAsDataURL(file);
  };

  // Base profile uses props for immediate display
  const profile = {
    name: user?.name || "Student",
    id: user?.enrollment_no || "N/A",
    department: user?.department || "General",
    year: user?.year ? `${user.year}` : "N/A",
    email: user?.email || "N/A",
  };

  return (
    <div className="max-w-6xl mx-auto pb-10 font-sans">
      
      {/* Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column */}
        <div className="space-y-6">
          
          {/* Profile Card */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-8 flex flex-col items-center text-center">
            <div className="w-32 h-32 rounded-full overflow-hidden mb-6 border-4 border-slate-50 relative group">
               <img
                 src={profilePhoto || `https://ui-avatars.com/api/?name=${encodeURIComponent(profile.name)}&background=2563eb&color=fff&size=256`}
                 alt={profile.name}
                 className="w-full h-full object-cover"
               />
               <button
                 onClick={() => fileInputRef.current?.click()}
                 disabled={uploadingPhoto}
                 className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
               >
                 <Camera className="w-6 h-6 text-white" />
               </button>
               <input
                 ref={fileInputRef}
                 type="file"
                 accept="image/*"
                 onChange={handlePhotoUpload}
                 className="hidden"
               />
            </div>
            
            <h2 className="text-2xl font-bold text-slate-800 mb-1">{profile.name}</h2>
            <p className="text-slate-500 font-medium mb-6">{profile.id}</p>
            
            <Link 
              to="/settings" 
              className="w-full py-2.5 bg-brand-blue hover:bg-blue-600 text-white font-semibold rounded-lg transition-colors"
            >
              Edit Profile
            </Link>
          </div>
          
          {/* Library Status */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
            <h3 className="text-base font-bold text-slate-900 mb-4">Library Status</h3>
            <div className="space-y-3">
              <div className="bg-green-100/60 text-green-700 px-4 py-2 rounded-lg text-sm font-semibold flex items-center justify-center">
                Active Membership
              </div>
              <div className="bg-blue-100/60 text-blue-700 px-4 py-2 rounded-lg text-sm font-semibold flex items-center justify-center">
                No Outstanding Fines
              </div>
            </div>
          </div>
          
        </div>
        
        {/* Right Column */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Academic Information */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-8">
            <h3 className="text-lg font-bold text-slate-900 mb-6">Academic Information</h3>
            
            <div className="space-y-0">
              <div className="flex flex-col sm:flex-row sm:items-center py-4 border-b border-slate-100 last:border-0 last:pb-0 font-medium">
                <span className="text-slate-400 w-48 shrink-0">Department</span>
                <span className="text-slate-800">{profile.department}</span>
              </div>
              
              <div className="flex flex-col sm:flex-row sm:items-center py-4 border-b border-slate-100 last:border-0 last:pb-0 font-medium">
                <span className="text-slate-400 w-48 shrink-0">Year of Study</span>
                <span className="text-slate-800">{profile.year}</span>
              </div>
              
              <div className="flex flex-col sm:flex-row sm:items-center py-4 border-b border-slate-100 last:border-0 last:pb-0 font-medium">
                <span className="text-slate-400 w-48 shrink-0">Email Address</span>
                <span className="text-slate-800">{profile.email}</span>
              </div>
            </div>
          </div>
          
          {/* Borrowing Privileges */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-8">
            <h3 className="text-lg font-bold text-slate-900 mb-6">Borrowing Privileges</h3>
            
            <div className="space-y-0">
              <div className="flex flex-col sm:flex-row sm:items-center py-4 border-b border-slate-100 last:border-0 last:pb-0 font-medium">
                <span className="text-slate-400 w-48 shrink-0">Max Books Allowed</span>
                <span className="text-slate-800">
                   {loading ? <Skeleton className="h-5 w-24" /> : error ? <span className="text-red-400 text-sm">Error</span> : `${policies?.max_books} Books`}
                </span>
              </div>
              
              <div className="flex flex-col sm:flex-row sm:items-center py-4 border-b border-slate-100 last:border-0 last:pb-0 font-medium">
                <span className="text-slate-400 w-48 shrink-0">Loan Duration</span>
                <span className="text-slate-800">
                   {loading ? <Skeleton className="h-5 w-20" /> : error ? <span className="text-red-400 text-sm">Error</span> : policies?.loan_duration}
                </span>
              </div>
              
              <div className="flex flex-col sm:flex-row sm:items-center py-4 border-b border-slate-100 last:border-0 last:pb-0 font-medium">
                <span className="text-slate-400 w-48 shrink-0">Renewal Limits</span>
                <span className="text-slate-800">
                   {loading ? <Skeleton className="h-5 w-40" /> : error ? <span className="text-red-400 text-sm">Error</span> : policies?.renewal_limit}
                </span>
              </div>
            </div>
          </div>
          
           {/* Account & Security */}
           <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-8">
            <h3 className="text-lg font-bold text-slate-900 mb-6">Account & Security</h3>
            
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 py-2">
              <div>
                <span className="text-slate-800 font-medium block mb-1">Password</span>
                <span className="text-slate-400 text-sm flex items-center gap-2">
                   Last changed on 
                   {loading ? <Skeleton className="h-4 w-24 translate-y-0.5" /> : error ? 'Unknown' : policies?.password_last_changed}
                </span>
              </div>
              <Link to="/settings" className="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg transition-colors text-sm">
                Change Password
              </Link>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}
