import { useState, useEffect } from 'react';
import axios from 'axios';
import { Book, CheckCircle2, AlertCircle, Clock, Calendar, ArrowLeft, History, BookOpen } from 'lucide-react';
import EmptyState from '../components/ui/EmptyState';
import { SkeletonCard } from '../components/ui/Skeleton';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

// Reusing the cover generator for consistency
const getCoverStyle = (title) => {
    // Simple hash to pick a color based on title length/chars
    const colors = [
        'from-blue-600 to-indigo-700',
        'from-emerald-500 to-teal-700',
        'from-orange-500 to-rose-700',
        'from-purple-600 to-fuchsia-800',
        'from-cyan-600 to-blue-800',
        'from-pink-600 to-rose-800',
        'from-amber-500 to-orange-700',
        'from-slate-600 to-slate-800'
    ];
    const index = title.length % colors.length;
    return colors[index];
};

export default function MyBooks() {
  const navigate = useNavigate();
  const [data, setData] = useState({ borrows: [], history: [] });
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('current'); // current, returned, all

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const { data } = await axios.get('/api/dashboard');
      setData({ borrows: data.borrows || [], history: data.history || [] });
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const currentBorrows = data.borrows.filter(b => b.status !== 'returned');
  const returnedBooks = data.history.filter(h => h.status === 'returned');
  const allBooks = [...data.borrows, ...data.history];

  const getDisplayBooks = () => {
    switch (activeTab) {
      case 'current': return currentBorrows;
      case 'returned': return returnedBooks;
      case 'all': return allBooks;
      default: return currentBorrows;
    }
  };

  const displayBooks = getDisplayBooks();

  if (loading) return <MyBooksSkeleton />;

  return (
    <div className="min-h-screen bg-slate-50/50 dark:bg-slate-950 pb-20 transition-colors">
      
      {/* 1. Glass Header & Stats */}
      <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200/50 dark:border-slate-800 sticky top-0 z-30 transition-colors">
          <div className="max-w-5xl mx-auto px-4 py-6">
            <div className="flex items-center gap-4 mb-6">
                <button onClick={() => navigate('/')} className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors text-slate-500 dark:text-slate-400">
                    <ArrowLeft size={20} />
                </button>
                <div>
                    <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight transition-colors">My Library</h1>
                    <p className="text-xs font-medium text-slate-500 dark:text-slate-400 transition-colors">Track your reading journey</p>
                </div>
            </div>

            <div className="grid grid-cols-3 gap-4">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100/50 dark:from-blue-900/20 dark:to-blue-800/20 border border-blue-100 dark:border-blue-800/50 rounded-xl p-4 flex flex-col items-center justify-center text-center shadow-sm relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-16 h-16 bg-blue-200/30 dark:bg-blue-600/10 rounded-bl-full -mr-8 -mt-8"></div>
                    <span className="text-3xl font-black text-blue-600 dark:text-blue-400 mb-1">{currentBorrows.length}</span>
                    <span className="text-xs font-bold uppercase tracking-wider text-blue-400 dark:text-blue-500">Active</span>
                </div>
                
                <div className="bg-gradient-to-br from-red-50 to-red-100/50 dark:from-red-900/20 dark:to-red-800/20 border border-red-100 dark:border-red-800/50 rounded-xl p-4 flex flex-col items-center justify-center text-center shadow-sm relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-16 h-16 bg-red-200/30 dark:bg-red-600/10 rounded-bl-full -mr-8 -mt-8"></div>
                    <span className="text-3xl font-black text-red-600 dark:text-red-400 mb-1">{currentBorrows.filter(b => b.status === 'overdue').length}</span>
                    <span className="text-xs font-bold uppercase tracking-wider text-red-400 dark:text-red-500">Overdue</span>
                </div>

                <div className="bg-gradient-to-br from-emerald-50 to-emerald-100/50 dark:from-emerald-900/20 dark:to-emerald-800/20 border border-emerald-100 dark:border-emerald-800/50 rounded-xl p-4 flex flex-col items-center justify-center text-center shadow-sm relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-16 h-16 bg-emerald-200/30 dark:bg-emerald-600/10 rounded-bl-full -mr-8 -mt-8"></div>
                    <span className="text-3xl font-black text-emerald-600 dark:text-emerald-400 mb-1">{returnedBooks.length}</span>
                    <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 dark:text-emerald-500">Read</span>
                </div>
            </div>

            {/* Tabs */}
            <div className="flex p-1 bg-slate-100 dark:bg-slate-800 rounded-xl mt-6 transition-colors">
                {['current', 'returned', 'all'].map((tab) => (
                    <button
                        key={tab}
                        onClick={() => setActiveTab(tab)}
                        className={`flex-1 py-2 rounded-lg text-sm font-bold transition-all ${
                            activeTab === tab 
                            ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' 
                            : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200'
                        }`}
                    >
                        {tab.charAt(0).toUpperCase() + tab.slice(1)}
                    </button>
                ))}
            </div>
          </div>
      </div>

      {/* 2. Book List */}
      <div className="max-w-5xl mx-auto px-4 py-8">
        <AnimatePresence mode="wait">
            {displayBooks.length === 0 ? (
                 <motion.div 
                    initial={{ opacity: 0, y: 10 }} 
                    animate={{ opacity: 1, y: 0 }} 
                    exit={{ opacity: 0, y: -10 }}
                    key="empty"
                 >
                    <EmptyState
                        icon={activeTab === 'returned' ? History : BookOpen}
                        title={activeTab === 'current' ? 'No active loans' : 'No history found'}
                        description={activeTab === 'current' ? 'You have no books currently checked out.' : 'Your reading history will appear here.'}
                        actionLabel="Browse Catalogue"
                        onAction={() => navigate('/books')}
                    />
                 </motion.div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {displayBooks.map((book, idx) => (
                        <motion.div
                            key={`${idx}-${book.book_id}`}
                            layout
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            transition={{ duration: 0.2, delay: idx * 0.05 }}
                            className="bg-white dark:bg-slate-900 rounded-2xl p-4 shadow-sm border border-slate-100 dark:border-slate-800 hover:shadow-md transition-all flex gap-5 group overflow-hidden relative"
                        >
                            {/* 3D Mini Cover */}
                            <div className="shrink-0 w-24 perspective-1000 relative z-10">
                                <div className={`relative aspect-[2/3] rounded-r-md shadow-lg transform transition-transform duration-300 group-hover:rotate-y-12 bg-gradient-to-br ${getCoverStyle(book.title)} flex items-center justify-center p-2 text-center`}>
                                     <div className="absolute inset-0 bg-black/10"></div>
                                     <Book className="text-white/30 absolute bottom-2 right-2" size={32} />
                                     <span className="text-[9px] font-bold text-white uppercase tracking-wider relative z-10 line-clamp-2 leading-tight">
                                         {book.title}
                                     </span>
                                     
                                     {/* Status Ribbon on Cover */}
                                     {book.status === 'overdue' && (
                                         <div className="absolute top-2 -right-2 bg-red-500 text-white text-[8px] font-bold px-2 py-0.5 transform rotate-2 shadow-sm">Overdue</div>
                                     )}
                                     {book.status === 'returned' && (
                                         <div className="absolute top-2 -right-2 bg-emerald-500 text-white text-[8px] font-bold px-2 py-0.5 transform rotate-2 shadow-sm">Returned</div>
                                     )}
                                </div>
                            </div>

                            {/* Details */}
                            <div className="flex-1 min-w-0 py-1 flex flex-col">
                                <div className="flex justify-between items-start gap-2">
                                    <div>
                                        <h3 className="font-bold text-slate-800 dark:text-white text-lg leading-tight mb-1 transition-colors">{book.title}</h3>
                                        <p className="text-sm font-medium text-slate-500 dark:text-slate-400 transition-colors">{book.author || 'Unknown Author'}</p>
                                    </div>
                                    {/* Quick Actions / Status Icon */}
                                    {book.status === 'overdue' ? (
                                        <AlertCircle className="text-red-500 shrink-0" size={20} />
                                    ) : book.status === 'returned' ? (
                                        <CheckCircle2 className="text-emerald-500 shrink-0" size={20} />
                                    ) : (
                                        <Clock className="text-blue-500 shrink-0" size={20} />
                                    )}
                                </div>
                                
                                <div className="mt-auto space-y-2">
                                    {/* Dates Grid */}
                                    <div className="grid grid-cols-2 gap-2 text-xs font-medium text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-800 p-2 rounded-lg transition-colors">
                                        <div>
                                            <span className="block text-[10px] uppercase text-slate-400 font-bold">Borrowed</span>
                                            {new Date(book.borrow_date || book.borrowed_date).toLocaleDateString()}
                                        </div>
                                        <div>
                                            {book.return_date ? (
                                                <>
                                                    <span className="block text-[10px] uppercase text-emerald-500 font-bold">Returned</span>
                                                    <span className="text-emerald-700">{new Date(book.return_date).toLocaleDateString()}</span>
                                                </>
                                            ) : (
                                                <>
                                                    <span className={`block text-[10px] uppercase font-bold ${book.status === 'overdue' ? 'text-red-500' : 'text-slate-400'}`}>Due Date</span>
                                                    <span className={book.status === 'overdue' ? 'text-red-600 font-bold' : ''}>
                                                        {new Date(book.due_date).toLocaleDateString()}
                                                    </span>
                                                </>
                                            )}
                                        </div>
                                    </div>

                                    {/* Alerts */}
                                    {book.status === 'overdue' && book.fine && (
                                        <div className="flex items-center gap-2 text-xs font-bold text-red-600 bg-red-50 px-3 py-1.5 rounded-lg">
                                            <span>Fine: ₹{book.fine}</span>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            )}
        </AnimatePresence>
      </div>
    </div>
  );
}

function MyBooksSkeleton() {
    return (
        <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
            <div className="h-8 w-48 bg-slate-200 dark:bg-slate-800 rounded-lg animate-pulse"></div>
            <div className="grid grid-cols-3 gap-4">
                {[1,2,3].map(i => <div key={i} className="h-24 bg-slate-200 dark:bg-slate-800 rounded-xl animate-pulse"></div>)}
            </div>
            <div className="h-10 w-full bg-slate-200 dark:bg-slate-800 rounded-xl animate-pulse"></div>
            <div className="grid grid-cols-2 gap-6">
                {[1,2,3,4].map(i => <div key={i} className="h-40 bg-slate-200 dark:bg-slate-800 rounded-2xl animate-pulse"></div>)}
            </div>
        </div>
    )
}
