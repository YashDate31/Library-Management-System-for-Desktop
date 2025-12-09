import { useState, useEffect } from 'react';
import axios from 'axios';
import { Book, Clock, AlertCircle, Award, Bell, User, X, ScanLine } from 'lucide-react';
import RequestModal from '../components/RequestModal';
import { Link } from 'react-router-dom';
import Skeleton, { SkeletonCard } from '../components/ui/Skeleton';
import ErrorMessage from '../components/ui/ErrorMessage';

export default function Dashboard({ user }) {
  const [data, setData] = useState({ 
    borrows: [], 
    history: [], 
    notices: [], 
    notifications: [],
    recent_requests: [],
    analytics: { badges: [], stats: {} }
  });
  const [loading, setLoading] = useState(true);
  const [profileModalOpen, setProfileModalOpen] = useState(false);

  useEffect(() => {
    fetchData();
  }, [profileModalOpen]);

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

  if (loading) return (
    <div className="space-y-8 pb-10">
       {/* Skeleton Profile */}
       <div className="bg-white rounded-[2rem] p-8 shadow-sm border border-slate-100 flex gap-10">
          <Skeleton className="w-40 h-40 rounded-full shrink-0" />
          <div className="flex-1 pt-4 space-y-4">
            <Skeleton className="h-8 w-1/3" />
            <Skeleton className="h-4 w-1/4" />
            <div className="grid grid-cols-2 gap-8 mt-8">
               <Skeleton className="h-12 w-full" />
               <Skeleton className="h-12 w-full" />
            </div>
          </div>
       </div>
       {/* Skeleton Grid */}
       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <SkeletonCard />
          <SkeletonCard />
          <SkeletonCard />
       </div>
    </div>
  );

  if (!data && !loading) return (
    <div className="p-10">
      <ErrorMessage 
        message="Failed to load your dashboard. Please check your connection."
        onRetry={fetchData}
      />
    </div>
  );

  const overdueBooks = data.borrows.filter(b => b.status === 'overdue');

  return (
    <div className="space-y-8 pb-10">
      <RequestModal 
        isOpen={profileModalOpen} 
        onClose={() => setProfileModalOpen(false)}
        title="Request Profile Update"
        type="profile_update"
        defaultDetails="Please update my phone number/email to: "
      />

      {/* 1. Alert Banner */}
      {overdueBooks.length > 0 && (
        <div className="w-full bg-red-100 border border-red-200 rounded-xl p-4 flex items-center justify-between text-red-800 shadow-sm animate-fade-in">
           <div className="flex items-center gap-4">
             <div className="w-8 h-8 rounded-full bg-red-600 flex items-center justify-center text-white shrink-0">
                <AlertCircle size={18} fill="currentColor" className="text-white" />
             </div>
             <span className="font-medium text-lg">Alert: '{overdueBooks[0].title}' is overdue by {overdueBooks[0].days_msg.replace('Overdue by ', '')}!</span>
           </div>
           <button className="hover:bg-red-200 p-2 rounded-lg transition text-red-800"><X size={20} /></button>
        </div>
      )}

      {/* 2. Profile Card */}
      <div className="bg-white rounded-[2rem] p-8 shadow-sm border border-slate-100 flex flex-col md:flex-row gap-10 items-center md:items-start">
         {/* Avatar Section */}
         <div className="shrink-0">
            <div className="w-40 h-40 rounded-full border-[6px] border-white shadow-xl overflow-hidden bg-slate-100 relative">
               {/* Placeholder for realistic avatar or user image */}
               <img 
                 src="https://images.unsplash.com/photo-1599566150163-29194dcaad36?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80" 
                 alt="Profile" 
                 className="w-full h-full object-cover"
               />
            </div>
         </div>

         {/* Info Grid */}
         <div className="flex-1 w-full pt-2">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-20 gap-y-8">
               <div className="space-y-1">
                  <p className="text-sm text-slate-400 font-medium">Name</p>
                  <p className="text-xl font-semibold text-slate-800">{user.name}</p>
               </div>
               <div className="space-y-1">
                  <p className="text-sm text-slate-400 font-medium">Enrollment No.</p>
                  <p className="text-xl font-semibold text-slate-800">{user.enrollment_no}</p>
               </div>
               <div className="space-y-1">
                  <p className="text-sm text-slate-400 font-medium">Department</p>
                  <p className="text-xl font-semibold text-slate-800">{user.department}</p>
               </div>
               <div className="space-y-1">
                  <p className="text-sm text-slate-400 font-medium">Year</p>
                  <p className="text-xl font-semibold text-slate-800">{user.year}</p>
               </div>
               <div className="col-span-2 space-y-1">
                  <p className="text-sm text-slate-400 font-medium">Email</p>
                  <p className="text-xl font-semibold text-slate-800">{user.email || 'john.doe@university.edu'}</p>
               </div>
            </div>
         </div>
      </div>

      {/* 3. Section Title */}
      <div>
        <h3 className="text-3xl font-bold text-slate-900 mb-8">
          Currently Borrowed
        </h3>

        {/* 4. Book Grid */}
        {data.borrows.length === 0 ? (
          <div className="bg-slate-50 border border-dashed border-slate-200 rounded-xl p-16 text-center text-slate-400">
             <Book size={48} className="mx-auto mb-4 opacity-20" />
             <p className="text-lg">No active loans.</p>
             <Link to="/books" className="text-blue-500 hover:underline mt-2 inline-block font-medium">Browse Catalogue</Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {data.borrows.map((book, i) => (
              <Book3DCard key={i} book={book} />
            ))}
          </div>
        )}
      </div>

      {/* 5. Lower Section (Trophies/Notices - optional keeping for functionality but styling to match) */}
      
    </div>
  );
}

// --- Sub Components ---

function Book3DCard({ book }) {
  const isOverdue = book.status === 'overdue';
  
  // Using specific teal color from mockup for normal books, white/minimal for others if needed.
  // Mockup shows teal backgrounds.
  
  return (
    <div className="flex flex-col bg-white rounded-3xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
        {/* Book Cover Representation */}
        <div className={`relative aspect-[3/4] rounded-lg shadow-2xl mb-6 overflow-hidden group transform transition-transform duration-500 hover:scale-[1.02] ${isOverdue ? 'bg-white' : 'bg-[#2A9D8F]'}`}>
           {/* Spine Highlight */}
           <div className="absolute left-0 top-0 bottom-0 w-3 bg-black/10 z-10"></div>
           
           <div className="absolute inset-0 p-8 flex flex-col items-center justify-center text-center">
              {/* Mockup styles - if it's the specific book 'JAVA PROGRAMMING' or generic */}
              <h3 className={`font-sans text-2xl font-bold tracking-wider uppercase leading-tight ${isOverdue ? 'text-slate-800' : 'text-white'}`}>
                {book.title}
              </h3>
              <div className={`w-12 h-0.5 my-6 ${isOverdue ? 'bg-slate-300' : 'bg-white/40'}`}></div>
              <p className={`text-xs uppercase tracking-widest font-medium ${isOverdue ? 'text-slate-500' : 'text-white/80'}`}>
                {book.author}
              </p>
           </div>
           
           {/* Texture/Sheen */}
           <div className="absolute inset-0 bg-gradient-to-tr from-black/5 to-white/10 pointer-events-none"></div>
        </div>

        {/* Info below card */}
        <div className="space-y-3">
           <div className="flex justify-between items-start">
              <h4 className="font-bold text-lg text-slate-900 leading-tight w-3/4">{book.title}</h4>
              {isOverdue && (
                  <span className="bg-red-100 text-red-600 text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wide">Overdue</span>
              )}
           </div>
           
           <div className="flex justify-between items-center text-sm">
             <span className="text-slate-500">Due: {book.due_date}</span>
             {isOverdue ? (
                <span className="font-bold text-red-500">Fine: ₹50</span>
             ) : (
                <span className="bg-amber-100 text-amber-700 text-xs font-bold px-3 py-1 rounded-full">Due in {book.days_msg.replace('Due in ', '').replace(' days', '')} days</span>
             )}
           </div>
        </div>
    </div>
  );
}

