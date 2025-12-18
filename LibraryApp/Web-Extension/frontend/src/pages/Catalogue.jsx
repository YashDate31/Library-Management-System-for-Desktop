import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useToast } from '../context/ToastContext';
import { Search, BookOpen, LayoutGrid, Monitor, Code, Globe, Database, Network, Cpu, Book, Layers, SlidersHorizontal, CheckCircle2, XCircle } from 'lucide-react';
import RequestModal from '../components/RequestModal';
import BookDetailModal from '../components/BookDetailModal';
import EmptyState from '../components/ui/EmptyState';
import { SkeletonCard } from '../components/ui/Skeleton';
import ErrorMessage from '../components/ui/ErrorMessage';
import ActiveFilters from '../components/ActiveFilters';
import { motion, AnimatePresence } from 'framer-motion';

const CATEGORY_ICONS = {
  'Core CS': Monitor,
  'Programming': Code,
  'Web Development': Globe,
  'Database': Database,
  'AI/ML': Cpu,
  'Networking': Network,
  'Software Engineering': Layers,
  'Project Guides': Book,
  'Competitive Programming': Code
};

// Generative book cover colors based on category/title hash
const getCoverStyle = (category) => {
    const styles = {
        'Core CS': 'from-slate-800 to-slate-900',
        'Programming': 'from-blue-600 to-indigo-700',
        'Web Development': 'from-emerald-500 to-teal-700',
        'Database': 'from-orange-500 to-rose-700',
        'AI/ML': 'from-purple-600 to-fuchsia-800',
        'Networking': 'from-cyan-600 to-blue-800',
        'Software Engineering': 'from-pink-600 to-rose-800',
        'Project Guides': 'from-amber-500 to-orange-700',
        'Competitive Programming': 'from-red-600 to-red-800'
    };
    return styles[category] || 'from-slate-600 to-slate-800';
};

export default function Catalogue() {
  const navigate = useNavigate();
  const { addToast } = useToast();
  const [books, setBooks] = useState([]);
  const [categories, setCategories] = useState([{ name: 'All', icon: LayoutGrid }]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Filter States
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [availabilityFilter, setAvailabilityFilter] = useState('all'); // 'all', 'available', 'out_of_stock'
  
  // UI States
  const [requestModalOpen, setRequestModalOpen] = useState(false);
  const [detailModalOpen, setDetailModalOpen] = useState(false);
  const [selectedBook, setSelectedBook] = useState(null);
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const { data } = await axios.get('/api/books');
      setBooks(data.books || []);
      
      // Process dynamic categories
      if (data.categories) {
        const dynamicCats = data.categories.map(catName => ({
          name: catName,
          icon: CATEGORY_ICONS[catName] || BookOpen
        }));
        setCategories([{ name: 'All', icon: LayoutGrid }, ...dynamicCats]);
      }
    } catch (e) {
      console.error(e);
      setError("Failed to load books. Please check your connection.");
      setBooks([]);
    } finally {
      setLoading(false);
    }
  };

  const handleBookClick = (book) => {
    setSelectedBook(book);
    setDetailModalOpen(true);
  };

  const filteredBooks = books.filter(book => {
    const matchesSearch = book.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          book.author.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || book.category === selectedCategory;
    const isAvailable = book.available_copies > 0;
    let matchesAvailability = true;
    if (availabilityFilter === 'available') matchesAvailability = isAvailable;
    if (availabilityFilter === 'out_of_stock') matchesAvailability = !isAvailable;

    return matchesSearch && matchesCategory && matchesAvailability;
  });

  if (loading) return <CatalogueSkeleton />;
  if (error) return <div className="p-10"><ErrorMessage message={error} onRetry={fetchBooks} /></div>;

  return (
    <div className="min-h-screen bg-slate-50/50 dark:bg-slate-950 pb-20 transition-colors">
      
      {/* 1. Glass Header & Search - Not sticky */}
      <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200/50 dark:border-slate-800 transition-colors">
          <div className="max-w-7xl mx-auto px-4 py-4 md:py-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  
                  {/* Title & Stats */}
                  <div>
                      <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight transition-colors">Catalogue</h1>
                      <p className="text-xs font-medium text-slate-500 dark:text-slate-400 transition-colors">{filteredBooks.length} titles available</p>
                  </div>

                  {/* Search Bar */}
                  <div className="flex-1 max-w-2xl relative group">
                      <div className="absolute inset-0 bg-blue-500/5 dark:bg-blue-500/20 rounded-2xl blur-xl group-focus-within:bg-blue-500/10 dark:group-focus-within:bg-blue-500/10 transition-colors"></div>
                      <div className="relative bg-white/50 dark:bg-slate-800/50 backdrop-blur-sm border border-slate-200 dark:border-slate-700 rounded-2xl flex items-center px-4 py-3 shadow-sm focus-within:shadow-md focus-within:border-blue-300 dark:focus-within:border-blue-500 transition-all">
                          <Search className="text-slate-400 mr-3 shrink-0" size={20} />
                          <input 
                              type="text" 
                              placeholder="Search titles, authors, ISBN..." 
                              className="bg-transparent border-none outline-none text-slate-700 dark:text-white w-full placeholder:text-slate-400 font-medium"
                              value={searchTerm}
                              onChange={(e) => setSearchTerm(e.target.value)}
                          />
                          {searchTerm && (
                              <button onClick={() => setSearchTerm('')} className="ml-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
                                  <XCircle size={16} />
                              </button>
                          )}
                          <div className="h-6 w-px bg-slate-200 dark:bg-slate-700 mx-3 transition-colors"></div>
                          <button 
                            onClick={() => setShowFilters(!showFilters)}
                            className={`p-1.5 rounded-lg transition-colors ${showFilters || availabilityFilter !== 'all' ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-200'}`}
                          >
                              <SlidersHorizontal size={18} />
                          </button>
                      </div>
                  </div>
              </div>

              {/* Expandable Filters */}
              <AnimatePresence>
                  {showFilters && (
                      <motion.div 
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="overflow-hidden"
                      >
                          <div className="pt-4 flex gap-4">
                              <button 
                                onClick={() => setAvailabilityFilter('all')}
                                className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-colors ${availabilityFilter === 'all' ? 'bg-slate-800 dark:bg-white text-white dark:text-slate-900 border-slate-800 dark:border-white' : 'bg-white dark:bg-slate-900/50 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'}`}
                              >
                                All Status
                              </button>
                              <button 
                                onClick={() => setAvailabilityFilter('available')}
                                className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-colors ${availabilityFilter === 'available' ? 'bg-emerald-600 text-white border-emerald-600' : 'bg-white dark:bg-slate-900/50 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'}`}
                              >
                                Available Now
                              </button>
                              <button 
                                onClick={() => setAvailabilityFilter('out_of_stock')}
                                className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-colors ${availabilityFilter === 'out_of_stock' ? 'bg-orange-500 text-white border-orange-500' : 'bg-white dark:bg-slate-900/50 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'}`}
                              >
                                Out of Stock
                              </button>
                          </div>
                      </motion.div>
                  )}
              </AnimatePresence>

              {/* Category Ribbon */}
              <div className="flex gap-2 mt-6 overflow-x-auto pb-2 -mx-4 px-4 scrollbar-hide">
                  {categories.map((cat) => {
                      const Icon = cat.icon;
                      const isActive = selectedCategory === cat.name;
                      return (
                          <button
                              key={cat.name}
                              onClick={() => setSelectedCategory(cat.name)}
                              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold whitespace-nowrap transition-all duration-300 ${
                                  isActive 
                                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30 scale-105' 
                                  : 'bg-white dark:bg-slate-800 text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700 hover:border-slate-300'
                              }`}
                          >
                              <Icon size={16} className={isActive ? 'opacity-100' : 'opacity-70'} />
                              {cat.name}
                          </button>
                      );
                  })}
              </div>
          </div>
      </div>

      {/* 2. Book Grid */}
      <div className="max-w-7xl mx-auto px-4 py-8">
          <motion.div 
            className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-x-6 gap-y-10"
            layout
          >
            <AnimatePresence mode='popLayout'>
                {filteredBooks.length > 0 ? (
                    filteredBooks.map((book) => (
                        <motion.div
                            key={book.book_id}
                            layout
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            transition={{ duration: 0.2 }}
                            onClick={() => handleBookClick(book)}
                            className="group cursor-pointer perspective-1000"
                        >
                            {/* 3D Cover */}
                            <div className="relative aspect-[2/3] mb-4 transition-all duration-300 transform group-hover:-translate-y-3 group-hover:rotate-x-2">
                                {/* Spine/Pages Effect */}
                                <div className="absolute top-1 right-1 w-full h-full bg-slate-200 rounded-r-sm shadow-md border-l border-slate-300"></div>
                                <div className="absolute top-2 right-2 w-full h-full bg-slate-100 rounded-r-sm shadow-sm border-l border-slate-300"></div>
                                
                                {/* Main Cover */}
                                <div className={`absolute inset-0 rounded-r-md shadow-xl group-hover:shadow-2xl transition-shadow bg-gradient-to-br ${getCoverStyle(book.category)} flex flex-col p-4 text-white overflow-hidden`}>
                                    <div className="absolute inset-0 bg-black/10 group-hover:bg-transparent transition-colors"></div>
                                    <div className="absolute -right-4 -bottom-4 text-white/10 opacity-50">
                                        <Book size={120} />
                                    </div>
                                    
                                    <div className="relative z-10 flex flex-col h-full">
                                        <div className="text-[10px] font-bold tracking-widest uppercase opacity-75 border-b border-white/20 pb-2 mb-2">
                                            {book.category}
                                        </div>
                                        <h3 className="font-serif font-bold text-lg leading-tight line-clamp-3 mb-1">
                                            {book.title}
                                        </h3>
                                        <p className="text-xs font-medium opacity-90 italic">
                                            {book.author}
                                        </p>
                                        
                                        <div className="mt-auto pt-4 flex items-center justify-between">
                                            {/* Department Badge */}
                                            <span className="text-[9px] bg-white/20 px-1.5 py-0.5 rounded backdrop-blur-sm">
                                                GPA Lib
                                            </span>
                                        </div>
                                    </div>
                                    
                                    {/* Sheen Effect */}
                                    <div className="absolute inset-0 bg-gradient-to-tr from-white/0 via-white/10 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"></div>
                                </div>
                            </div>
                            
                            {/* Details Below */}
                            <div className="space-y-1 px-1">
                                <h4 className="font-bold text-slate-800 dark:text-white text-sm leading-tight truncate px-1 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                                    {book.title}
                                </h4>
                                <div className="flex items-center justify-between px-1">
                                    <span className="text-xs text-slate-500 dark:text-slate-400 font-medium truncate max-w-[60%]">
                                        {book.author}
                                    </span>
                                    {book.available_copies > 0 ? (
                                        <span className="flex items-center gap-1 text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full">
                                            <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
                                            {book.available_copies} Left
                                        </span>
                                    ) : (
                                        <span className="text-[10px] font-bold text-orange-600 bg-orange-50 px-2 py-0.5 rounded-full">
                                            Taken
                                        </span>
                                    )}
                                </div>
                            </div>
                        </motion.div>
                    ))
                ) : (
                    <div className="col-span-full py-12">
                        <EmptyState 
                            icon={BookOpen}
                            title="No books found"
                            description="Try changing your filters or search terms."
                        />
                    </div>
                )}
            </AnimatePresence>
          </motion.div>
      </div>

      <RequestModal 
        isOpen={requestModalOpen} 
        onClose={() => setRequestModalOpen(false)} 
        title={`Request Notification: ${selectedBook?.title}`}
        type="availability_notification"
        defaultDetails={`Please notify me when '${selectedBook?.title}' becomes available.`}
      />
      
      <BookDetailModal
        isOpen={detailModalOpen}
        onClose={() => setDetailModalOpen(false)}
        bookId={selectedBook?.book_id}
      />
    </div>
  );
}

function CatalogueSkeleton() {
    return (
        <div className="min-h-screen bg-slate-50/50 dark:bg-slate-950 pb-20">
             <div className="bg-white/80 dark:bg-slate-900/80 border-b border-slate-200/50 dark:border-slate-800 px-4 py-8 mb-8">
                 <div className="max-w-7xl mx-auto space-y-6">
                     <div className="h-8 w-48 bg-slate-200 dark:bg-slate-800 rounded-lg animate-pulse"></div>
                     <div className="h-12 w-full max-w-2xl bg-slate-100 dark:bg-slate-900 rounded-2xl animate-pulse"></div>
                     <div className="flex gap-3">
                         {[1,2,3,4,5].map(i => <div key={i} className="h-9 w-24 bg-slate-200 dark:bg-slate-800 rounded-xl animate-pulse"></div>)}
                     </div>
                 </div>
             </div>
             <div className="max-w-7xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8">
                 {[1,2,3,4,5,6,7,8,9,10].map(i => (
                     <div key={i} className="space-y-3">
                         <div className="aspect-[2/3] bg-slate-200 dark:bg-slate-800 rounded-md animate-pulse"></div>
                         <div className="h-4 w-3/4 bg-slate-200 dark:bg-slate-800 rounded animate-pulse"></div>
                         <div className="h-3 w-1/2 bg-slate-200 dark:bg-slate-800 rounded animate-pulse"></div>
                     </div>
                 ))}
             </div>
        </div>
    )
}
