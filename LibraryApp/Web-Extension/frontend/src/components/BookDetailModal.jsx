import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { X, BookOpen, Clock, AlertCircle, CheckCircle, Calendar, User, Tag, Hash } from 'lucide-react';

export default function BookDetailModal({ isOpen, onClose, bookId }) {
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [requestStatus, setRequestStatus] = useState(null); // 'idle', 'loading', 'success', 'error'

  useEffect(() => {
    if (isOpen && bookId) {
      fetchBookDetails();
      setRequestStatus('idle');
    } else {
      setBook(null); // Reset when closed
    }
  }, [isOpen, bookId]);

  const fetchBookDetails = async () => {
    setLoading(true);
    setError(null);
    try {
      const { data } = await axios.get(`/api/books/${bookId}`);
      setBook(data);
    } catch (err) {
      console.error("Error fetching book details:", err);
      setError("Failed to load book details. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleRequestBook = async () => {
    setRequestStatus('loading');
    try {
      await axios.post('/api/request', {
        type: 'book_request',
        details: `Request for book: ${book.title} (ID: ${book.book_id})`
      });
      setRequestStatus('success');
      // Optional: Refresh book details to show updated count if logic existed
    } catch (err) {
      console.error("Refuest failed:", err);
      setRequestStatus('error');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity" 
        onClick={onClose}
      />

      {/* Modal Content */}
      <div className="relative w-full max-w-2xl bg-white rounded-2xl shadow-2xl overflow-hidden animate-fade-in-up flex flex-col max-h-[90vh]">
        
        {/* Header / Loading State */}
        {loading ? (
           <div className="p-12 flex flex-col items-center justify-center space-y-4">
             <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
             <p className="text-slate-500 font-medium">Loading details...</p>
           </div>
        ) : error ? (
           <div className="p-12 flex flex-col items-center justify-center text-center space-y-4">
             <div className="w-16 h-16 bg-red-100 text-red-500 rounded-full flex items-center justify-center mb-2">
                <AlertCircle size={32} />
             </div>
             <h3 className="text-xl font-bold text-slate-800">Oops!</h3>
             <p className="text-slate-500 max-w-xs">{error}</p>
             <button onClick={onClose} className="px-6 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-lg transition-colors">
               Close
             </button>
           </div>
        ) : book && (
          <>
             {/* Close Button */}
             <button 
               onClick={onClose}
               className="absolute top-4 right-4 z-10 p-2 bg-black/5 hover:bg-black/10 rounded-full text-slate-500 hover:text-slate-800 transition-colors"
             >
               <X size={20} />
             </button>

             <div className="flex flex-col md:flex-row h-full overflow-hidden">
                {/* Visual Side (Left) */}
                <div className="w-full md:w-2/5 bg-slate-50 p-8 flex items-center justify-center relative overflow-hidden">
                   <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5" />
                   
                   {/* Book Cover Mockup */}
                   <div className="w-40 h-60 bg-white shadow-2xl relative transform transition-transform hover:scale-105 duration-500 z-10 rounded-r-md border-l-4 border-slate-200">
                      <div className="absolute inset-0 p-4 flex flex-col items-center justify-center text-center">
                         <h2 className="font-serif font-bold text-slate-800 leading-tight mb-2 line-clamp-3">{book.title}</h2>
                         <p className="text-xs uppercase tracking-widest text-slate-400">{book.author?.split(' ')[0]}</p>
                         <div className="mt-8 w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-slate-300">
                           <BookOpen size={20} />
                         </div>
                      </div>
                   </div>
                </div>

                {/* Details Side (Right) */}
                <div className="flex-1 p-8 overflow-y-auto">
                   
                   {/* Categories & Tags */}
                   <div className="flex flex-wrap gap-2 mb-4">
                      <span className="px-3 py-1 bg-blue-50 text-blue-700 text-xs font-bold uppercase tracking-wider rounded-full">
                        {book.category || 'General'}
                      </span>
                      {book.status === 'borrowed' && (
                        <span className="px-3 py-1 bg-amber-50 text-amber-700 text-xs font-bold uppercase tracking-wider rounded-full flex items-center gap-1">
                          <Clock size={12} /> Currently Borrowed
                        </span>
                      )}
                   </div>

                   <h2 className="text-2xl md:text-3xl font-bold text-slate-900 mb-2 leading-tight">{book.title}</h2>
                   <p className="text-lg text-slate-500 font-medium mb-6">by {book.author}</p>

                   {/* Stats Grid */}
                   <div className="grid grid-cols-2 gap-4 mb-8">
                      <div className="p-3 bg-slate-50 rounded-lg">
                         <div className="flex items-center gap-2 text-slate-400 mb-1">
                            <Hash size={14} /> <span className="text-xs font-bold uppercase">ISBN</span>
                         </div>
                         <p className="font-mono text-sm text-slate-700">{book.isbn || 'N/A'}</p>
                      </div>
                      <div className="p-3 bg-slate-50 rounded-lg">
                         <div className="flex items-center gap-2 text-slate-400 mb-1">
                            <Tag size={14} /> <span className="text-xs font-bold uppercase">ID</span>
                         </div>
                         <p className="font-mono text-sm text-slate-700">#{book.book_id}</p>
                      </div>
                      <div className="p-3 bg-slate-50 rounded-lg col-span-2">
                         <div className="flex items-center gap-2 text-slate-400 mb-1">
                            <BookOpen size={14} /> <span className="text-xs font-bold uppercase">Availability</span>
                         </div>
                         <div className="flex items-center gap-2">
                            <div className={`w-3 h-3 rounded-full ${book.available_copies > 0 ? 'bg-green-500' : 'bg-red-500'}`} />
                            <p className="font-bold text-slate-700">
                               {book.available_copies > 0 
                                 ? `${book.available_copies} of ${book.total_copies} copies available` 
                                 : 'Out of Stock'
                               }
                            </p>
                         </div>
                      </div>
                   </div>

                   {/* Description (If available, otherwise placeholder) */}
                   <div className="mb-8">
                      <h4 className="text-sm font-bold text-slate-900 mb-2">Description</h4>
                      <p className="text-slate-600 text-sm leading-relaxed">
                        {book.description || "No description available for this title. Please check with the librarian for more details or preview the book in the physical library."}
                      </p>
                   </div>

                   {/* Action Buttons */}
                   {requestStatus === 'success' ? (
                      <div className="p-4 bg-green-50 border border-green-100 rounded-xl flex items-center gap-3 text-green-700">
                         <CheckCircle size={24} />
                         <div>
                            <p className="font-bold">Request Submitted!</p>
                            <p className="text-xs">The librarian has been notified.</p>
                         </div>
                      </div>
                   ) : (
                      <button 
                        onClick={handleRequestBook}
                        disabled={requestStatus === 'loading' || book.available_copies <= 0}
                        className={`w-full py-4 rounded-xl font-bold text-white flex items-center justify-center gap-2 transition-all shadow-lg active:scale-[0.99] ${
                           book.available_copies > 0 
                             ? 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-blue-500/25' 
                             : 'bg-slate-300 cursor-not-allowed text-slate-500 shadow-none'
                        }`}
                      >
                        {requestStatus === 'loading' ? (
                           <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : book.available_copies > 0 ? (
                           <>Request Book <span className="text-white/60 font-normal">| Pick up at Library</span></>
                        ) : (
                           'Currently Unavailable'
                        )}
                      </button>
                   )}
                   
                   {requestStatus === 'error' && (
                     <p className="text-red-500 text-xs mt-2 text-center font-medium">
                       Something went wrong. Please try again.
                     </p>
                   )}

                </div>
             </div>
          </>
        )}
      </div>
    </div>
  );
}
