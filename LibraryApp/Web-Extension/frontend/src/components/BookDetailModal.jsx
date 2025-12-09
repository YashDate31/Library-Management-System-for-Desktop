import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { X, BookOpen, Clock, AlertCircle, CheckCircle, Calendar, User, Tag, Hash, Heart, Share2, Star } from 'lucide-react';

export default function BookDetailModal({ isOpen, onClose, bookId }) {
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [requestStatus, setRequestStatus] = useState('idle'); // 'idle', 'loading', 'success', 'error'
  const [isWishlisted, setIsWishlisted] = useState(false);

  useEffect(() => {
    if (isOpen && bookId) {
      fetchBookDetails();
      setRequestStatus('idle');
      setIsWishlisted(false); // Reset/Mock
    } else {
      setBook(null); 
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
    } catch (err) {
      console.error("Request failed:", err);
      setRequestStatus('error');
    }
  };

  const toggleWishlist = () => {
    setIsWishlisted(!isWishlisted);
    // Future: API call to sync wishlist
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 isolate">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity animate-in fade-in duration-200" 
        onClick={onClose}
      />

      {/* Modal Card */}
      <div className="relative w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden animate-fade-in-up flex flex-col md:flex-row max-h-[90vh] md:h-[600px]">
        
        {loading ? (
           <div className="w-full h-full flex flex-col items-center justify-center space-y-4">
             <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
             <p className="text-slate-500 font-medium animate-pulse">Fetching book details...</p>
           </div>
        ) : error ? (
           <div className="w-full h-full p-12 flex flex-col items-center justify-center text-center space-y-4">
             <div className="w-16 h-16 bg-red-100 text-red-500 rounded-full flex items-center justify-center mb-2">
                <AlertCircle size={32} />
             </div>
             <h3 className="text-xl font-bold text-slate-800">Unable to load book</h3>
             <p className="text-slate-500 max-w-xs">{error}</p>
             <button onClick={onClose} className="px-6 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-lg transition-colors">
               Close
             </button>
           </div>
        ) : book && (
          <>
             {/* Close Button Mobile (Absolute) */}
             <button 
               onClick={onClose}
               className="md:hidden absolute top-4 right-4 z-20 p-2 bg-black/20 hover:bg-black/30 text-white rounded-full backdrop-blur-md transition-colors"
             >
               <X size={20} />
             </button>

             {/* LEFT COLUMN: Visual & Meta */}
             <div className="w-full md:w-1/3 bg-slate-900 relative flex flex-col items-center p-8 text-white overflow-hidden shrink-0">
                {/* Background Pattern */}
                <div className="absolute inset-0 opacity-10 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] mix-blend-overlay" />
                <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 to-purple-600/20" />
                
                {/* Book Cover */}
                <div className="relative z-10 w-40 md:w-48 aspect-[2/3] shadow-2xl rounded-sm group perspective-1000 mb-6">
                   <div className="w-full h-full bg-slate-200 rounded-sm overflow-hidden relative shadow-lg transform transition-transform group-hover:rotate-y-12 duration-500">
                      {/* Image Placeholder or Actual Image */}
                      <div className="absolute inset-0 bg-gradient-to-br from-slate-200 to-slate-300 flex items-center justify-center">
                         <BookOpen size={48} className="text-slate-400 opacity-50" />
                      </div>
                      {/* Spine Effect */}
                      <div className="absolute left-0 top-0 bottom-0 w-2 bg-black/10 z-20" />
                   </div>
                </div>

                {/* Quick Stats - Mobile Hidden usually, but let's show here */}
                <div className="relative z-10 text-center space-y-1">
                   <h3 className="font-bold text-lg leading-tight">{book.title}</h3>
                   <p className="text-slate-400 text-sm">{book.author}</p>
                   <div className="flex items-center justify-center gap-1 text-amber-400 text-sm mt-2">
                      <Star size={14} fill="currentColor" />
                      <span className="font-bold">4.5</span>
                      <span className="text-slate-500 text-xs ml-1">(24 reviews)</span>
                   </div>
                </div>
             </div>

             {/* RIGHT COLUMN: Details & Actions */}
             <div className="flex-1 bg-white flex flex-col min-h-0">
                
                {/* Fixed Header (Desktop) */}
                <div className="hidden md:flex items-center justify-between px-8 py-6 border-b border-slate-100 shrink-0">
                   <div className="flex items-center gap-3">
                      <span className="px-3 py-1 bg-blue-50 text-blue-700 text-xs font-bold uppercase tracking-wider rounded-full">
                        {book.category || 'General'}
                      </span>
                      {book.status === 'borrowed' && (
                        <span className="px-3 py-1 bg-amber-50 text-amber-700 text-xs font-bold uppercase tracking-wider rounded-full flex items-center gap-1">
                          <Clock size={12} /> Borrowed
                        </span>
                      )}
                   </div>
                   <div className="flex items-center gap-2">
                      <button onClick={toggleWishlist} className={`p-2 rounded-full transition-colors ${isWishlisted ? 'bg-pink-50 text-pink-500' : 'hover:bg-slate-100 text-slate-400'}`}>
                         <Heart size={20} fill={isWishlisted ? "currentColor" : "none"} />
                      </button>
                      <button className="p-2 hover:bg-slate-100 text-slate-400 rounded-full transition-colors">
                         <Share2 size={20} />
                      </button>
                      <button onClick={onClose} className="p-2 hover:bg-slate-100 text-slate-400 rounded-full transition-colors ml-2">
                         <X size={24} />
                      </button>
                   </div>
                </div>

                {/* Scrollable Content */}
                <div className="flex-1 overflow-y-auto p-6 md:p-8">
                   {/* Mobile Title (Visible only on mobile) */}
                   <div className="md:hidden mb-6">
                      <div className="flex items-center justify-between mb-2">
                         <span className="px-3 py-1 bg-blue-50 text-blue-700 text-xs font-bold uppercase tracking-wider rounded-full">
                           {book.category || 'General'}
                         </span>
                         <div className="flex gap-2">
                            <button onClick={toggleWishlist}><Heart size={20} className={isWishlisted ? 'text-pink-500 fill-current' : 'text-slate-400'} /></button>
                            <button><Share2 size={20} className="text-slate-400" /></button>
                         </div>
                      </div>
                      <h2 className="text-2xl font-bold text-slate-900 mb-1">{book.title}</h2>
                   </div>

                   {/* Description */}
                   <div className="mb-8">
                      <h4 className="text-sm font-bold text-slate-900 mb-3 uppercase tracking-wide">About this Book</h4>
                      <p className="text-slate-600 text-sm md:text-base leading-relaxed">
                        {book.description || "No description available. Access detailed summaries, author bios, and reviews by visiting the physical library or checking the external database linked below."}
                      </p>
                   </div>

                   {/* Metadata Grid */}
                   <div className="grid grid-cols-2 md:grid-cols-3 gap-6 mb-8 pb-8 border-b border-slate-100">
                      <div>
                         <span className="text-xs font-bold text-slate-400 uppercase block mb-1">ISBN</span>
                         <span className="text-sm font-mono text-slate-700">{book.isbn || '978-3-16-148410-0'}</span>
                      </div>
                      <div>
                         <span className="text-xs font-bold text-slate-400 uppercase block mb-1">Publisher</span>
                         <span className="text-sm text-slate-700 font-medium">{book.publisher || 'Tech Press Inc.'}</span>
                      </div>
                      <div>
                         <span className="text-xs font-bold text-slate-400 uppercase block mb-1">Pages</span>
                         <span className="text-sm text-slate-700 font-medium">{book.page_count || '342'} pages</span>
                      </div>
                      <div>
                         <span className="text-xs font-bold text-slate-400 uppercase block mb-1">Language</span>
                         <span className="text-sm text-slate-700 font-medium">English</span>
                      </div>
                      <div>
                         <span className="text-xs font-bold text-slate-400 uppercase block mb-1">Format</span>
                         <span className="text-sm text-slate-700 font-medium">Hardcover</span>
                      </div>
                   </div>

                   {/* Availability Section */}
                   <div>
                      <h4 className="text-sm font-bold text-slate-900 mb-4 uppercase tracking-wide flex items-center gap-2">
                        <BookOpen size={16} /> Live Availability
                      </h4>
                      
                      <div className="bg-slate-50 rounded-xl p-4 border border-slate-100">
                         <div className="flex items-center justify-between mb-3">
                            <span className="font-bold text-slate-700">Main Library</span>
                            <span className={`text-sm font-bold px-2 py-1 rounded-md ${book.available_copies > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                               {book.available_copies > 0 ? 'Available' : 'Out of Stock'}
                            </span>
                         </div>
                         <div className="w-full bg-slate-200 rounded-full h-2 mb-2 overflow-hidden">
                            <div 
                              className="bg-green-500 h-2 rounded-full transition-all duration-500" 
                              style={{ width: `${(book.available_copies / book.total_copies) * 100}%` }}
                            />
                         </div>
                         <p className="text-xs text-slate-500 text-right">
                            {book.available_copies} of {book.total_copies} copies available
                         </p>
                      </div>
                   </div>
                </div>

                {/* Footer / Actions */}
                <div className="p-6 border-t border-slate-100 bg-white shrink-0">
                   {requestStatus === 'success' ? (
                      <div className="w-full py-3 bg-green-50 border border-green-100 rounded-xl flex items-center justify-center gap-2 text-green-700 animate-fade-in">
                         <CheckCircle size={20} />
                         <span className="font-bold">Request Submitted Successfully</span>
                      </div>
                   ) : (
                      <div className="flex gap-3">
                         <button 
                           onClick={handleRequestBook}
                           disabled={requestStatus === 'loading' || book.available_copies <= 0}
                           className={`flex-1 py-3.5 rounded-xl font-bold text-white flex items-center justify-center gap-2 transition-all shadow-lg active:scale-[0.98] ${
                              book.available_copies > 0 
                                ? 'bg-brand-blue hover:bg-blue-600 shadow-blue-500/25' 
                                : 'bg-slate-300 cursor-not-allowed text-slate-500'
                           }`}
                         >
                           {requestStatus === 'loading' ? (
                              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                           ) : book.available_copies > 0 ? (
                              <>Request Book</>
                           ) : (
                              'Unavailable'
                           )}
                         </button>
                         {book.available_copies <= 0 && (
                            <button className="px-4 py-3.5 rounded-xl border-2 border-slate-200 font-bold text-slate-600 hover:border-slate-300 hover:bg-slate-50 transition-colors">
                               Notify Me
                            </button>
                         )}
                      </div>
                   )}
                </div>

             </div>
          </>
        )}
      </div>
    </div>
  );
}
