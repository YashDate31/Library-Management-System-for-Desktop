import { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Filter, BookOpen, Clock, LayoutGrid, Monitor, FlaskConical, History, ChevronDown, Calendar, Copy, Bell, ArrowRight, Code, Globe, Database, Network, Cpu, Book, Layers, X } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import RequestModal from '../components/RequestModal';
import BookDetailModal from '../components/BookDetailModal';
import EmptyState from '../components/ui/EmptyState';

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

export default function Catalogue() {
  const navigate = useNavigate();
  const [books, setBooks] = useState([]);
  const [categories, setCategories] = useState([{ name: 'All', icon: LayoutGrid }]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Filter States
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [availabilityFilter, setAvailabilityFilter] = useState('all'); // 'all', 'available', 'out_of_stock'
  
  // UI States
  const [activeDropdown, setActiveDropdown] = useState(null); // 'category', 'availability', or null
  const [requestModalOpen, setRequestModalOpen] = useState(false);
  const [detailModalOpen, setDetailModalOpen] = useState(false);
  const [selectedBook, setSelectedBook] = useState(null);

  const availabilityOptions = [
    { id: 'all', label: 'All Status' },
    { id: 'available', label: 'Available Now' },
    { id: 'out_of_stock', label: 'Out of Stock' }
  ];

  useEffect(() => {
    fetchBooks();
  }, []);

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = () => setActiveDropdown(null);
    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
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
    // 1. Search Filter
    const matchesSearch = book.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          book.author.toLowerCase().includes(searchTerm.toLowerCase());
    
    // 2. Category Filter
    const matchesCategory = selectedCategory === 'All' || book.category === selectedCategory;
    
    // 3. Availability Filter
    const isAvailable = book.available_copies > 0;
    let matchesAvailability = true;
    if (availabilityFilter === 'available') matchesAvailability = isAvailable;
    if (availabilityFilter === 'out_of_stock') matchesAvailability = !isAvailable;

    return matchesSearch && matchesCategory && matchesAvailability;
  });

  if (loading) return <div className="p-10 text-center text-text-secondary animate-pulse">Loading Library...</div>;

  return (
    <div className="space-y-10 pb-20" onClick={() => setActiveDropdown(null)}>
      
      {/* Header Section */}
      <div>
        <h1 className="text-4xl font-black text-slate-900 mb-2 tracking-tight">Book Discovery</h1>
        <p className="text-slate-500 text-lg">Find your next read from thousands of titles available in the library.</p>
      </div>

      {/* Search & Toolbar */}
      <div className="flex flex-col md:flex-row gap-4 relative z-20">
         {/* Search Bar */}
         <div className="flex-1 bg-slate-100 rounded-lg flex items-center px-4 py-3">
            <Search className="text-slate-400 mr-3" size={20} />
            <input 
              type="text" 
              placeholder="Search by title, author, category..." 
              className="bg-transparent border-none outline-none text-slate-700 w-full placeholder:text-slate-400 font-medium"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
         </div>

         {/* Right Side Filters */}
         <div className="flex gap-3">
            {/* Category Dropdown */}
            <div className="relative" onClick={e => e.stopPropagation()}>
                <button 
                  onClick={() => setActiveDropdown(activeDropdown === 'category' ? null : 'category')}
                  className={`flex items-center gap-2 px-5 py-3 rounded-lg font-semibold transition-colors border ${
                    activeDropdown === 'category' || selectedCategory !== 'All' 
                      ? 'bg-blue-50 text-blue-600 border-blue-200' 
                      : 'bg-slate-100 text-slate-700 border-transparent hover:bg-slate-200'
                  }`}
                >
                   <Filter size={18} /> 
                   <span className="max-w-[100px] truncate">{selectedCategory === 'All' ? 'Category' : selectedCategory}</span>
                   <ChevronDown size={16} className={`transition-transform ${activeDropdown === 'category' ? 'rotate-180' : ''}`} />
                </button>
                
                {activeDropdown === 'category' && (
                  <div className="absolute top-full right-0 mt-2 w-64 bg-white rounded-xl shadow-xl border border-slate-100 overflow-hidden animate-fade-in z-50">
                     {categories.map((cat) => (
                       <button
                         key={cat.name}
                         onClick={() => {
                           setSelectedCategory(cat.name);
                           setActiveDropdown(null);
                         }}
                         className={`w-full text-left px-4 py-3 text-sm font-medium hover:bg-slate-50 flex items-center gap-3 transition-colors ${
                            selectedCategory === cat.name ? 'text-blue-600 bg-blue-50/50' : 'text-slate-600'
                         }`}
                       >
                         {/* Icon placeholder if needed, or simple text */}
                         {cat.name}
                         {selectedCategory === cat.name && <div className="ml-auto w-2 h-2 rounded-full bg-blue-600"></div>}
                       </button>
                     ))}
                  </div>
                )}
            </div>

            {/* Availability Dropdown */}
            <div className="relative" onClick={e => e.stopPropagation()}>
                <button 
                  onClick={() => setActiveDropdown(activeDropdown === 'availability' ? null : 'availability')}
                  className={`flex items-center gap-2 px-5 py-3 rounded-lg font-semibold transition-colors border ${
                    activeDropdown === 'availability' || availabilityFilter !== 'all'
                      ? 'bg-blue-50 text-blue-600 border-blue-200' 
                      : 'bg-slate-100 text-slate-700 border-transparent hover:bg-slate-200'
                  }`}
                >
                   <Calendar size={18} /> 
                   {availabilityOptions.find(o => o.id === availabilityFilter)?.label || 'Availability'}
                   <ChevronDown size={16} className={`transition-transform ${activeDropdown === 'availability' ? 'rotate-180' : ''}`} />
                </button>

                {activeDropdown === 'availability' && (
                  <div className="absolute top-full right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-slate-100 overflow-hidden animate-fade-in z-50">
                     {availabilityOptions.map((opt) => (
                       <button
                         key={opt.id}
                         onClick={() => {
                           setAvailabilityFilter(opt.id);
                           setActiveDropdown(null);
                         }}
                         className={`w-full text-left px-4 py-3 text-sm font-medium hover:bg-slate-50 flex items-center gap-3 transition-colors ${
                            availabilityFilter === opt.id ? 'text-blue-600 bg-blue-50/50' : 'text-slate-600'
                         }`}
                       >
                         {opt.label}
                         {availabilityFilter === opt.id && <div className="ml-auto w-2 h-2 rounded-full bg-blue-600"></div>}
                       </button>
                     ))}
                  </div>
                )}
            </div>
         </div>
      </div>

      {/* Category Pills */}
      <div className="flex flex-wrap gap-3">
         {categories.map((cat) => {
           const Icon = cat.icon;
           const isActive = selectedCategory === cat.name;
           return (
             <button
               key={cat.name}
               onClick={() => setSelectedCategory(cat.name)}
               className={`flex items-center gap-2 px-5 py-2.5 rounded-lg font-medium transition-all duration-200 ${
                 isActive 
                   ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/30' 
                   : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
               }`}
             >
               <Icon size={18} />
               {cat.name}
             </button>
           );
         })}
      </div>

      {/* Active Filters Display */}
      {(searchTerm || selectedCategory !== 'All' || availabilityFilter !== 'all') && (
        <div className="flex items-center gap-2 flex-wrap animate-fade-in">
           <span className="text-sm font-bold text-slate-500 mr-2">Active Filters:</span>
           
           {searchTerm && (
             <button onClick={() => setSearchTerm('')} className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 text-slate-700 text-xs font-bold rounded-full hover:bg-slate-200 transition-colors">
               Search: "{searchTerm}" <X size={14} />
             </button>
           )}

           {selectedCategory !== 'All' && (
             <button onClick={() => setSelectedCategory('All')} className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-50 text-blue-700 text-xs font-bold rounded-full hover:bg-blue-100 transition-colors">
               {selectedCategory} <X size={14} />
             </button>
           )}

           {availabilityFilter !== 'all' && (
             <button onClick={() => setAvailabilityFilter('all')} className="flex items-center gap-1.5 px-3 py-1.5 bg-green-50 text-green-700 text-xs font-bold rounded-full hover:bg-green-100 transition-colors">
               {availabilityOptions.find(o => o.id === availabilityFilter)?.label} <X size={14} />
             </button>
           )}

           <button 
             onClick={() => { setSearchTerm(''); setSelectedCategory('All'); setAvailabilityFilter('all'); }}
             className="text-xs font-bold text-red-500 hover:text-red-700 hover:underline ml-2"
           >
             Clear All
           </button>
        </div>
      )}

      {/* Book Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-8">
        {filteredBooks.length > 0 ? (
          filteredBooks.map(book => (
            <BookCard 
              key={book.book_id} 
              book={book} 
              onClick={() => handleBookClick(book)} 
            />
          ))
        ) : (

          <div className="col-span-full">
             <EmptyState
                icon={BookOpen}
                title="No books found"
                description="We couldn't find any books matching your current filters. Try adjusting your search terms or category."
                actionLabel="Clear all filters"
                onAction={() => { setSearchTerm(''); setSelectedCategory('All'); setAvailabilityFilter('all'); }}
             />
          </div>
        )}
      </div>

      {/* Modals */}
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

function BookCard({ book, onClick }) {
  const isAvailable = book.available_copies > 0;
  
  // Dynamic color for category tag based on category content
  const getCategoryColor = (cat) => {
    if (cat.includes('Computer')) return 'text-emerald-500';
    if (cat.includes('Literature')) return 'text-orange-500';
    if (cat.includes('Physics')) return 'text-blue-500';
    if (cat.includes('History')) return 'text-red-500';
    return 'text-purple-500';
  };

  return (
    <div className="flex flex-col bg-white rounded-none md:rounded-xl overflow-hidden group">
       {/* Cover Image Area */}
       <div className="bg-slate-100 aspect-[4/5] relative p-8 flex items-center justify-center mb-4 rounded-xl overflow-hidden">
          {/* Mockup spine/cover look */}
          <div className="w-32 h-44 shadow-2xl relative bg-white transform transition-transform duration-500 group-hover:-translate-y-2 group-hover:scale-105">
              <div className="absolute inset-0 flex flex-col items-center justify-center p-4 text-center border-l-4 border-black/5 bg-slate-50">
                  <span className="text-[8px] uppercase tracking-widest text-slate-400 mb-2">{book.author.split(' ')[0]}</span>
                  <h4 className="font-serif font-bold text-slate-800 text-sm leading-tight line-clamp-3">{book.title}</h4>
                  <div className="w-8 h-8 rounded-full bg-slate-200 mt-4 mix-blend-multiply"></div>
              </div>
          </div>
       </div>

       {/* Content */}
       <div className="flex-1 flex flex-col px-1">
          <p className={`text-xs font-bold uppercase tracking-widest mb-2 ${getCategoryColor(book.category)}`}>
            {book.category}
          </p>
          <h3 className="text-xl font-bold text-slate-900 leading-tight mb-2 group-hover:text-blue-600 transition-colors cursor-pointer" onClick={onClick}>
            {book.title}
          </h3>
          <p className="text-slate-500 font-medium text-sm mb-4">{book.author}</p>

          <div className="mt-auto space-y-4">
             {/* Availability Status */}
             <div className="flex items-center gap-2 text-sm font-medium">
                <span className={`w-2.5 h-2.5 rounded-full ${isAvailable ? 'bg-green-500' : 'bg-slate-400'}`}></span>
                <span className={isAvailable ? 'text-green-700' : 'text-slate-500'}>
                   {isAvailable ? `${book.available_copies} Available` : 'Out of Stock'}
                </span>
             </div>

             {/* Action Button */}
             <button 
                onClick={onClick}
                className="w-full py-2.5 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition-all active:scale-[0.98] shadow-md shadow-blue-500/20"
             >
                View Details
             </button>
          </div>
       </div>
    </div>
  );
}
