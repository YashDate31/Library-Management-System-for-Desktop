import { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Filter, BookOpen } from 'lucide-react';

export default function Catalogue() {
  const [books, setBooks] = useState([]);
  const [categories, setCategories] = useState([]);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('');
  const [loading, setLoading] = useState(true);

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

  return (
    <div>
      <div className="glass p-6 rounded-2xl mb-8 flex flex-col md:flex-row gap-4 items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Library Catalogue</h2>
          <p className="text-slate-500">Browse and search available resources</p>
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
              className="pl-10 pr-8 py-2.5 rounded-xl border border-slate-200 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none bg-white appearance-none"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            >
              <option value="">All Categories</option>
              {categories.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-20">Loading books...</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {books.map(book => (
            <div key={book.book_id} className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm hover:shadow-lg hover:-translate-y-1 transition group">
              <div className="h-40 bg-slate-50 rounded-xl mb-4 flex items-center justify-center text-slate-300 group-hover:text-primary transition-colors">
                <BookOpen size={48} />
              </div>
              
              <div className="mb-4">
                <span className="text-xs font-bold text-primary bg-primary/10 px-2 py-1 rounded-md">{book.category}</span>
                <h3 className="font-bold text-slate-800 mt-2 line-clamp-1">{book.title}</h3>
                <p className="text-sm text-slate-500 line-clamp-1">by {book.author}</p>
              </div>
              
              <div className="flex justify-between items-center text-sm pt-4 border-t border-slate-50">
                <span className="text-slate-400">ID: {book.book_id}</span>
                <span className={`font-semibold px-2 py-0.5 rounded-full text-xs ${book.total_copies > 0 ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-600'}`}>
                  {book.total_copies > 0 ? 'Available' : 'Out of Stock'}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {!loading && books.length === 0 && (
        <div className="text-center py-20 text-slate-400">No books found matching your criteria.</div>
      )}
    </div>
  );
}
