import { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Filter, BookOpen, Bell } from 'lucide-react';
import RequestModal from '../components/RequestModal';

export default function Catalogue() {
  const [books, setBooks] = useState([]);
  const [categories, setCategories] = useState([]);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('');
  const [loading, setLoading] = useState(true);

  // Modal State
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedBook, setSelectedBook] = useState(null);

  useEffect(() => {
    fetchBooks();
  }, [search, filter]);

  const fetchBooks = async () => {
    try {
      const { data } = await axios.get('/api/books', {
        params: { q: search, category: filter }
      });
      setBooks(data.books);
      setCategories(data.categories);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleNotifyRequest = (book) => {
    setSelectedBook(book);
    setModalOpen(true);
  };

  return (
    <div>
      <RequestModal 
        isOpen={modalOpen} 
        onClose={() => setModalOpen(false)} 
        title={`Request Notification: ${selectedBook?.title}`}
        type="availability_notification"
        defaultDetails={`Please notify me when '${selectedBook?.title}' by ${selectedBook?.author} becomes available.`}
      />

      {/* Header & Search */}
      <div className="glass p-6 rounded-2xl mb-8 flex flex-col md:flex-row gap-4 items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Library Catalogue</h2>
          <p className="text-slate-500">Browse {books.length} available resources</p>
        </div>
        
        <div className="flex gap-3 w-full md:w-auto">
          <div className="relative flex-1 md:w-64">
            <Search className="absolute left-3 top-3 text-slate-400" size={20} />
            <input 
              type="text" 
              placeholder="Search title, author..." 
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          
          <div className="relative">
            <Filter className="absolute left-3 top-3 text-slate-400" size={20} />
            <select 
              className="pl-10 pr-8 py-2.5 rounded-xl border border-slate-200 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none bg-white appearance-none cursor-pointer"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            >
              <option value="">All Categories</option>
              {categories.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
        </div>
      </div>

      {/* Grid */}
      {loading ? (
        <div className="text-center py-20 text-slate-400 animate-pulse">Loading catalogue...</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {books.map(book => {
            const isAvailable = book.available_copies > 0;
            return (
              <div 
                key={book.book_id} 
                className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm hover:shadow-xl hover:-translate-y-2 transition-all duration-300 group flex flex-col h-full"
              >
                <div className="h-40 bg-slate-50 rounded-xl mb-4 flex items-center justify-center text-slate-300 group-hover:text-primary transition-colors relative overflow-hidden">
                   <div className="absolute inset-0 bg-gradient-to-tr from-primary/10 to-transparent opacity-0 group-hover:opacity-100 transition duration-500"></div>
                   <BookOpen size={48} className="relative z-10 transform group-hover:scale-110 transition-transform duration-300" />
                </div>
                
                <div className="mb-4 flex-1">
                  <span className="text-xs font-bold text-primary bg-primary/10 px-2 py-1 rounded-md">{book.category || 'General'}</span>
                  <h3 className="font-bold text-slate-800 mt-2 line-clamp-2">{book.title}</h3>
                  <p className="text-sm text-slate-500 line-clamp-1">by {book.author}</p>
                </div>
                
                <div className="flex justify-between items-center text-sm pt-4 border-t border-slate-50 mt-auto">
                  <span className={`font-semibold px-2 py-1 rounded-lg text-xs flex items-center gap-1 ${
                    isAvailable ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-600'
                  }`}>
                    {isAvailable ? (
                      <>Available ({book.available_copies})</>
                    ) : (
                      <>Out of Stock</>
                    )}
                  </span>
                  
                  {!isAvailable && (
                    <button 
                      onClick={() => handleNotifyRequest(book)}
                      className="text-primary hover:bg-primary/10 p-1.5 rounded-lg transition"
                      title="Notify when available"
                    >
                      <Bell size={16} />
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
      
      {!loading && books.length === 0 && (
        <div className="text-center py-20 text-slate-400">
          <BookOpen size={48} className="mx-auto mb-4 opacity-20" />
          <p>No books found matching your criteria.</p>
        </div>
      )}
    </div>
  );
}
