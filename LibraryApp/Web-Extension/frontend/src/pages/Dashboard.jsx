import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Book, AlertCircle, Clock, CheckCircle2, Megaphone, TrendingUp } from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Skeleton from '../components/ui/Skeleton';
import ErrorMessage from '../components/ui/ErrorMessage';
import EmptyState from '../components/ui/EmptyState';
import BookLoanCard from '../components/BookLoanCard';

export default function Dashboard({ user }) {
  const navigate = useNavigate();
  const [data, setData] = useState({ 
    borrows: [], 
    history: [], 
    notices: [], 
    notifications: [],
    recent_requests: [],
    analytics: { badges: [], stats: {} }
  });
  const [loading, setLoading] = useState(true);
  const [profilePhoto, setProfilePhoto] = useState(null);

  // Load profile photo from localStorage
  useEffect(() => {
    const savedPhoto = localStorage.getItem('profilePhoto');
    if (savedPhoto) {
      setProfilePhoto(savedPhoto);
    }
  }, []);

  // Use actual user data from session
  const displayUser = {
    name: user?.name || "Student",
    year: user?.year || "N/A",
    department: user?.department || "Computer Department",
    avatar: profilePhoto || `https://ui-avatars.com/api/?name=${encodeURIComponent(user?.name || 'Student')}&background=3b82f6&color=fff&size=128&bold=true`
  };

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const { data } = await axios.get('/api/dashboard');
      setData(data);
    } catch (e) {
      console.error("Failed to fetch dashboard, using fallback state if needed", e);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <DashboardSkeleton />;
  if (!data && !loading) return (
    <div className="p-6">
      <ErrorMessage message="Failed to load your dashboard." onRetry={fetchData} />
    </div>
  );

  const overdueBooks = (data.borrows || []).filter(b => b.status === 'overdue');
  const activeBorrows = data.borrows || [];

  const getLoanStatus = (book) => {
    if (book.status === 'overdue') return 'overdue';
    // Parser for "5 days left" logic
    const days = parseInt(book.days_msg?.replace(/\D/g, '') || '10', 10);
    if (days <= 3) return 'due_soon';
    return 'normal';
  };

  // Helper to safely format dates from "YYYY-MM-DD HH:MM:SS"
  const formatDate = (dateStr) => {
    if (!dateStr) return 'Recently';
    try {
        // Replace space with T for ISO compatibility
        const isoStr = dateStr.replace(' ', 'T');
        return new Date(isoStr).toLocaleDateString(undefined, { 
            month: 'short', 
            day: 'numeric', 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    } catch (e) {
        return dateStr;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50/50 pb-24 md:pb-10">

      <div className="px-4 py-6 space-y-8 max-w-4xl mx-auto">
        
        {/* 1. Profile & Quick Actions Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
             {/* Profile Card (Glassmorphism + Gradient) */}
            <div className="md:col-span-2 relative group">
                <div className="absolute inset-0 bg-blue-600 rounded-2xl blur opacity-20 group-hover:opacity-30 transition-opacity duration-500"></div>
                <Card className="relative h-full bg-gradient-to-br from-blue-600 to-indigo-700 text-white border-none shadow-2xl overflow-hidden flex flex-col justify-between p-6">
                    
                    {/* Background Pattern */}
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                        <svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                        </svg>
                    </div>

                    <div className="flex items-start gap-5 relative z-10">
                        <div className="shrink-0 relative">
                            <img 
                                src={displayUser.avatar} 
                                alt="Profile" 
                                className="w-16 h-16 rounded-full border-2 border-white/50 object-cover shadow-lg"
                            />
                            <div className="absolute bottom-0 right-0 w-3.5 h-3.5 bg-emerald-400 border-2 border-indigo-700 rounded-full"></div>
                        </div>
                        <div>
                            <p className="text-blue-100 text-xs font-medium tracking-wider uppercase mb-1">Student Portal</p>
                            <h2 className="text-2xl font-heading font-bold">{displayUser.name}</h2>
                            <div className="flex items-center text-blue-100/90 text-sm gap-2 mt-1">
                                <span>{displayUser.year}</span>
                                <span className="w-1 h-1 bg-blue-300 rounded-full"></span>
                                <span className="truncate max-w-[150px]">{displayUser.department}</span>
                            </div>
                        </div>
                    </div>

                    <div className="mt-8 flex items-end justify-between relative z-10">
                         <div className="flex gap-4">
                             <div className="bg-white/10 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-white/10">
                                 <span className="text-xs text-blue-100 block">ID Number</span>
                                 <span className="font-mono font-medium tracking-wide">{user?.enrollment_no || '---'}</span>
                             </div>
                         </div>
                         <Button 
                            variant="secondary" 
                            size="sm" 
                            className="bg-white/10 hover:bg-white/20 text-white border-transparent backdrop-blur-md"
                            onClick={() => navigate('/profile')}
                         >
                            View Profile
                         </Button>
                    </div>
                </Card>
            </div>

            {/* Quick Stats Grid */}
            <div className="grid grid-cols-1 gap-3 content-start">
                  <Card className="p-4 flex items-center justify-between hover:shadow-md transition-shadow">
                      <div>
                          <p className="text-xs text-slate-500 font-bold uppercase tracking-wide">Borrowed</p>
                          <p className="text-2xl font-black text-slate-800 mt-0.5">{activeBorrows.length}</p>
                      </div>
                      <div className="w-10 h-10 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center">
                          <Book size={20} />
                      </div>
                  </Card>
                  
                  <Card className="p-4 flex items-center justify-between hover:shadow-md transition-shadow">
                      <div>
                          <p className="text-xs text-slate-500 font-bold uppercase tracking-wide">Returned</p>
                          <p className="text-2xl font-black text-emerald-600 mt-0.5">{data.history?.length || 0}</p>
                      </div>
                      <div className="w-10 h-10 bg-emerald-50 text-emerald-600 rounded-full flex items-center justify-center">
                           <CheckCircle2 size={20} />
                      </div>
                  </Card>

                   <Card className="p-4 flex items-center justify-between hover:shadow-md transition-shadow">
                      <div>
                          <p className="text-xs text-slate-500 font-bold uppercase tracking-wide">Overdue</p>
                          <p className={`text-2xl font-black mt-0.5 ${overdueBooks.length > 0 ? 'text-red-600' : 'text-slate-400'}`}>
                              {overdueBooks.length}
                          </p>
                      </div>
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center ${overdueBooks.length > 0 ? 'bg-red-50 text-red-600' : 'bg-slate-100 text-slate-400'}`}>
                           <AlertCircle size={20} />
                      </div>
                  </Card>
            </div>
        </div>

        {/* 2. Broadcast Notices (Modernized) */}
        {data.notices && data.notices.length > 0 && (
           <div className="space-y-4">
             <div className="flex items-center gap-2 px-1">
                <Megaphone className="w-5 h-5 text-amber-500" />
                <h3 className="text-lg font-bold text-slate-800">Announcements</h3>
             </div>
             <div className="grid gap-4">
               {data.notices.map((notice) => (
                 <div key={notice.id} className="group relative bg-white border border-slate-200 p-5 rounded-xl shadow-sm hover:shadow-md transition-all duration-300 border-l-4 border-l-amber-400">
                     <span className="absolute top-4 right-4 text-[10px] font-bold tracking-wider text-slate-400 uppercase bg-slate-100 px-2 py-1 rounded-md">
                        {notice.title === 'Repo Update' ? 'System' : 'Notice'}
                     </span>
                     <h4 className="font-bold text-slate-800 text-lg mb-2 pr-12 group-hover:text-amber-600 transition-colors">
                        {notice.title}
                     </h4>
                     <p className="text-slate-600 text-sm leading-relaxed mb-3">
                        {notice.content}
                     </p>
                     <div className="flex items-center gap-2 text-xs text-slate-400 font-medium border-t border-slate-100 pt-3 mt-1">
                        <Clock size={12} />
                        <span>Posted on {formatDate(notice.date)}</span>
                     </div>
                 </div>
               ))}
             </div>
           </div>
        )}

        {/* 3. Security Alerts */}
        {data.notifications?.some(n => n.type === 'danger' && n.title === 'Security Alert') && (
           <div className="animate-fade-in">
              <div className="bg-red-50 border border-red-100 rounded-xl p-4 flex items-center justify-between shadow-sm">
                  <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-sm text-red-500">
                          <TrendingUp size={20} /> {/* Should be security icon really, but trending works for 'Action' */}
                      </div>
                      <div>
                          <h4 className="font-bold text-red-900">Security Action Required</h4>
                          <p className="text-sm text-red-700">You are using the default password.</p>
                      </div>
                  </div>
                  <Button variant="danger" size="sm" onClick={() => navigate('/settings')}>Fix Now</Button>
              </div>
           </div>
        )}

        {/* 4. Currently Borrowed */}
        <div>
           <div className="flex items-center justify-between mb-5 px-1">
             <h3 className="text-lg font-heading font-bold text-slate-800 flex items-center gap-2">
                <Book className="w-5 h-5 text-blue-600" />
                Current Reads
             </h3>
             <Button variant="ghost" size="sm" className="text-blue-600 hover:bg-blue-50" onClick={() => navigate('/history')}>
               View History
             </Button>
           </div>

           {activeBorrows.length === 0 ? (
             <EmptyState
               icon={Book}
               title="No books borrowed"
               description="Your reading list is empty. Explore the catalogue!"
               actionLabel="Find Books"
               onAction={() => navigate('/books')}
             />
           ) : (
             <div className="flex overflow-x-auto pb-6 -mx-4 px-4 gap-4 snap-x hide-scrollbar">
                {activeBorrows.map((book, i) => (
                  <div key={i} className="snap-center shrink-0 w-[280px]">
                    <BookLoanCard 
                      title={book.title}
                      author={book.author || "Unknown Author"}
                      dueDate={book.due_date}
                      status={getLoanStatus(book)}
                      fine="₹50" 
                      onViewDetails={() => navigate(`/books/${book.book_id}`)}
                    />
                  </div>
                ))}
             </div>
           )}
        </div>

      </div>
    </div>
  );
}

function DashboardSkeleton() {
  return (
    <div className="p-4 space-y-6 max-w-4xl mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
             <Skeleton className="h-48 w-full rounded-2xl" />
        </div>
        <div className="grid grid-cols-1 gap-3">
             <Skeleton className="h-20 w-full rounded-xl" />
             <Skeleton className="h-20 w-full rounded-xl" />
             <Skeleton className="h-20 w-full rounded-xl" />
        </div>
      </div>
      <Skeleton className="h-32 w-full rounded-2xl" />
      <div className="flex gap-4">
         <Skeleton className="h-64 w-[240px] rounded-2xl" />
         <Skeleton className="h-64 w-[240px] rounded-2xl" />
      </div>
    </div>
  );
}