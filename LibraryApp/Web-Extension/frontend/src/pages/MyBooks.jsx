import { useState, useEffect } from 'react';
import axios from 'axios';
import { Book, CheckCircle, AlertTriangle, Clock, Calendar, ArrowLeft } from 'lucide-react';
import EmptyState from '../components/ui/EmptyState';
import Skeleton from '../components/ui/Skeleton';
import { Link } from 'react-router-dom';

export default function MyBooks({ user }) {
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

  const getStatusBadge = (book) => {
    if (book.status === 'overdue') {
      return <span className="px-3 py-1 bg-red-100 text-red-700 text-xs font-bold rounded-full">Overdue</span>;
    }
    if (book.status === 'returned') {
      return <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-bold rounded-full">Returned</span>;
    }
    const daysLeft = parseInt(book.days_msg?.match(/\d+/)?.[0] || '10');
    if (daysLeft <= 3) {
      return <span className="px-3 py-1 bg-amber-100 text-amber-700 text-xs font-bold rounded-full">Due Soon</span>;
    }
    return <span className="px-3 py-1 bg-blue-100 text-blue-700 text-xs font-bold rounded-full">Active</span>;
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto space-y-6 pb-10">
        <Skeleton className="h-8 w-48" />
        <div className="space-y-4">
          <Skeleton className="h-32 w-full" />
          <Skeleton className="h-32 w-full" />
          <Skeleton className="h-32 w-full" />
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-10">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-900 mb-2">My Books</h1>
        <p className="text-slate-600">Track your borrowed books and reading history</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-xl p-4 border border-slate-100 text-center">
          <p className="text-slate-600 text-sm mb-1">Currently Borrowed</p>
          <p className="text-3xl font-black text-blue-600">{currentBorrows.length}</p>
        </div>
        <div className="bg-white rounded-xl p-4 border border-slate-100 text-center">
          <p className="text-slate-600 text-sm mb-1">Overdue</p>
          <p className="text-3xl font-black text-red-600">{currentBorrows.filter(b => b.status === 'overdue').length}</p>
        </div>
        <div className="bg-white rounded-xl p-4 border border-slate-100 text-center">
          <p className="text-slate-600 text-sm mb-1">Total Read</p>
          <p className="text-3xl font-black text-green-600">{returnedBooks.length}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-slate-200">
        <button
          onClick={() => setActiveTab('current')}
          className={`px-4 py-2 font-semibold transition-all ${
            activeTab === 'current'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-slate-500 hover:text-slate-700'
          }`}
        >
          Currently Borrowed ({currentBorrows.length})
        </button>
        <button
          onClick={() => setActiveTab('returned')}
          className={`px-4 py-2 font-semibold transition-all ${
            activeTab === 'returned'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-slate-500 hover:text-slate-700'
          }`}
        >
          Returned ({returnedBooks.length})
        </button>
        <button
          onClick={() => setActiveTab('all')}
          className={`px-4 py-2 font-semibold transition-all ${
            activeTab === 'all'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-slate-500 hover:text-slate-700'
          }`}
        >
          All History ({allBooks.length})
        </button>
      </div>

      {/* Books List */}
      {displayBooks.length === 0 ? (
        <EmptyState
          icon={Book}
          title={activeTab === 'current' ? 'No books borrowed' : activeTab === 'returned' ? 'No returned books' : 'No reading history'}
          description={activeTab === 'current' ? 'Start borrowing books from the catalogue to see them here.' : 'Your reading history will appear here once you return books.'}
          actionLabel="Browse Catalogue"
          onAction={() => window.location.href = '/books'}
        />
      ) : (
        <div className="space-y-4">
          {displayBooks.map((book, idx) => (
            <div key={idx} className="bg-white rounded-xl p-5 border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-start gap-4">
                {/* Book Icon */}
                <div className="w-16 h-20 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg flex items-center justify-center shrink-0">
                  <Book className="w-8 h-8 text-blue-600" />
                </div>

                {/* Book Details */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-4 mb-2">
                    <div>
                      <h3 className="text-lg font-bold text-slate-900 mb-1">{book.title}</h3>
                      <p className="text-sm text-slate-600">{book.author || 'Unknown Author'}</p>
                    </div>
                    {getStatusBadge(book)}
                  </div>

                  {/* Dates Info */}
                  <div className="flex flex-wrap gap-4 text-sm text-slate-600 mt-3">
                    <div className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      <span>Borrowed: {book.borrow_date || book.borrowed_date}</span>
                    </div>
                    {book.return_date && (
                      <div className="flex items-center gap-1">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span>Returned: {book.return_date}</span>
                      </div>
                    )}
                    {book.due_date && book.status !== 'returned' && (
                      <div className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        <span>Due: {book.due_date}</span>
                      </div>
                    )}
                  </div>

                  {/* Additional Info */}
                  {book.status === 'overdue' && book.fine && (
                    <div className="mt-3 p-3 bg-red-50 border border-red-100 rounded-lg flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4 text-red-600" />
                      <span className="text-sm text-red-700 font-semibold">
                        Fine: ₹{book.fine} ({book.days_msg || 'Overdue'})
                      </span>
                    </div>
                  )}

                  {book.status === 'returned' && book.fine_paid && (
                    <div className="mt-3 p-3 bg-amber-50 border border-amber-100 rounded-lg">
                      <span className="text-sm text-amber-700 font-semibold">
                        Fine Paid: ₹{book.fine_paid}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Back to Dashboard */}
      <Link
        to="/"
        className="inline-flex items-center gap-2 px-4 py-2 text-blue-600 hover:text-blue-700 font-semibold"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Dashboard
      </Link>
    </div>
  );
}
