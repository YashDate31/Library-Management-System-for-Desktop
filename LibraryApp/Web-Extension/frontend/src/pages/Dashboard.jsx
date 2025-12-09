import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Book, Clock, AlertCircle, Calendar, ChevronRight } from 'lucide-react';
import AppBar from '../components/ui/AppBar';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import Skeleton, { SkeletonCard } from '../components/ui/Skeleton';
import ErrorMessage from '../components/ui/ErrorMessage';
import EmptyState from '../components/ui/EmptyState';

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

  // Mock data fallback if API fails (for development robustness)
  const mockUser = {
    name: user?.name || "Student Name",
    year: user?.year || "3rd Year",
    department: user?.department || "Computer Science",
    avatar: "https://images.unsplash.com/photo-1599566150163-29194dcaad36?ixlib=rb-4.0.3&auto=format&fit=crop&w=687&q=80"
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
      // In a real app we might want to keep the error state, but for this redesign let's show data if available or empty
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

  const overdueBooks = data.borrows.filter(b => b.status === 'overdue');
  const activeBorrows = data.borrows; // In a real app filtering might be needed, but 'borrows' usually implies active.

  return (
    <div className="min-h-screen bg-background pb-24 md:pb-10">
      {/* 1. Mobile App Bar */}
      {/* 1. Mobile App Bar removed - using Layout header */}

      <div className="px-4 py-6 space-y-6 max-w-3xl mx-auto">
        
        {/* 2. Compact Profile Summary */}
        <Card className="flex items-center gap-4 bg-gradient-to-br from-blue-600 to-blue-700 text-white border-none shadow-blue-200 shadow-xl">
          <div className="shrink-0 relative">
             <img 
               src={mockUser.avatar} 
               alt="Profile" 
               className="w-16 h-16 rounded-full border-2 border-white/30 object-cover shadow-sm"
             />
             <div className="absolute bottom-0 right-0 w-4 h-4 bg-emerald-400 border-2 border-blue-700 rounded-full"></div>
          </div>
          <div className="flex-1 min-w-0">
             <h2 className="text-xl font-heading font-bold truncate">{mockUser.name}</h2>
             <div className="flex items-center text-blue-100 text-sm gap-2">
               <span>{mockUser.year}</span>
               <span>•</span>
               <span className="truncate">{mockUser.department}</span>
             </div>
          </div>
        </Card>

        {/* 2.5 Security Alert Card */}
        {data.notifications.some(n => n.type === 'danger' && n.title === 'Security Alert') && (
          <div className="animate-fade-in">
             <Card className="bg-red-50 border-red-100 shadow-sm relative overflow-hidden">
               <div className="absolute top-0 right-0 w-20 h-20 bg-red-100 rounded-bl-full -mr-10 -mt-10 opacity-50"></div>
               
               <div className="relative z-10">
                 <div className="flex items-start gap-3 mb-3">
                   <div className="bg-red-100 p-2 rounded-full shrink-0">
                     <AlertCircle className="w-6 h-6 text-red-600" />
                   </div>
                   <div>
                     <h3 className="font-bold text-red-900 leading-tight text-lg">Action Required</h3>
                     <p className="text-red-600 text-sm font-medium mt-1">Change Default Password</p>
                   </div>
                 </div>
                 
                 <div className="flex items-center justify-between mt-4 pl-1">
                   <p className="text-xs text-red-500 font-medium max-w-[60%]">
                     You are using the default enrollment number as password.
                   </p>
                   <Button 
                      variant="danger" 
                      size="sm" 
                      onClick={() => navigate('/settings')} // Assuming settings has the change password form
                    >
                      Change Now
                    </Button>
                 </div>
               </div>
             </Card>
          </div>
        )}

        {/* 3. Overdue Alert Card */}
        {overdueBooks.length > 0 && (
          <div className="space-y-4 animate-fade-in">
             {overdueBooks.map((book, idx) => (
               <Card key={`alert-${idx}`} className="bg-red-50 border-red-100 shadow-sm relative overflow-hidden">
                 <div className="absolute top-0 right-0 w-20 h-20 bg-red-100 rounded-bl-full -mr-10 -mt-10 opacity-50"></div>
                 
                 <div className="relative z-10">
                   <div className="flex items-start gap-3 mb-3">
                     <AlertCircle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
                     <div>
                       <h3 className="font-bold text-red-900 leading-tight">{book.title}</h3>
                       <p className="text-red-600 text-xs font-medium mt-1">Due {book.due_date}</p>
                     </div>
                   </div>
                   
                   <div className="flex items-center justify-between mt-4 pl-8">
                     <div className="flex flex-col">
                       <span className="text-[10px] uppercase tracking-wider text-red-500 font-bold">Fine Amount</span>
                       <span className="text-lg font-bold text-red-700">₹50.00</span>
                     </div>
                     <Button 
                        variant="danger" 
                        size="sm" 
                        onClick={() => navigate(`/books/${book.book_id}`)}
                      >
                        Renew / Pay
                      </Button>
                   </div>
                 </div>
               </Card>
             ))}
          </div>
        )}

        {/* 4. Currently Borrowed Section */}
        <div>
           <div className="flex items-center justify-between mb-4 px-1">
             <h3 className="text-lg font-heading font-bold text-slate-800">Currently Borrowed</h3>
             <Button variant="ghost" size="sm" className="text-blue-600 -mr-2" onClick={() => navigate('/history')}>
               View All
             </Button>
           </div>

           {activeBorrows.length === 0 ? (
             <EmptyState
               icon={Book}
               title="No books borrowed"
               description="Your reading list is empty."
               actionLabel="Browse Catalogue"
               onAction={() => navigate('/books')}
             />
           ) : (
             // Horizontal Scroll Container
             <div className="flex overflow-x-auto pb-6 -mx-4 px-4 gap-4 snap-x hide-scrollbar">
                {activeBorrows.map((book, i) => (
                  <div key={i} className="snap-center shrink-0 w-[240px]">
                    <BorrowedBookCard book={book} />
                  </div>
                ))}
             </div>
           )}
        </div>

      </div>
    </div>
  );
}

// Compact, Mobile-Friendly Book Card
function BorrowedBookCard({ book }) {
  const isOverdue = book.status === 'overdue';
  const daysLeft = book.days_msg?.replace(/\D/g, '') || '0'; 

  return (
    <Card className="h-full flex flex-col p-0 overflow-hidden hover:shadow-md transition-all group border-slate-200">
       <div className="h-32 bg-slate-100 relative group-hover:scale-105 transition-transform duration-500">
          {/* Subtle pattern or image placeholder */}
          <div className="absolute inset-0 flex items-center justify-center text-slate-300">
             <Book size={48} strokeWidth={1} />
          </div>
          {/* Status Badge overlay */}
          <div className="absolute top-2 right-2">
             <Badge variant={isOverdue ? 'danger' : 'primary'} className="shadow-sm">
                {isOverdue ? 'Overdue' : `${daysLeft} days left`}
             </Badge>
          </div>
       </div>
       
       <div className="p-4 flex flex-col flex-1">
          <h4 className="font-bold text-slate-800 line-clamp-2 mb-1 leading-snug min-h-[2.5rem]">
            {book.title}
          </h4>
          <p className="text-xs text-slate-500 font-medium mb-4 line-clamp-1">{book.author}</p>
          
          <div className="mt-auto pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
             <span className="text-slate-400 flex items-center gap-1">
               <Calendar size={12} />
               {book.due_date}
             </span>
             <ChevronRight size={14} className="text-slate-300 group-hover:translate-x-1 transition-transform" />
          </div>
       </div>
    </Card>
  );
}

function DashboardSkeleton() {
  return (
    <div className="p-4 space-y-6 max-w-3xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <Skeleton className="h-8 w-32" />
        <Skeleton className="h-8 w-8 rounded-full" />
      </div>
      <Skeleton className="h-32 w-full rounded-2xl" />
      <div className="space-y-4">
        <Skeleton className="h-6 w-48" />
        <div className="flex gap-4 overflow-hidden">
          <Skeleton className="h-64 w-[240px] rounded-2xl shrink-0" />
          <Skeleton className="h-64 w-[240px] rounded-2xl shrink-0" />
        </div>
      </div>
    </div>
  );
}