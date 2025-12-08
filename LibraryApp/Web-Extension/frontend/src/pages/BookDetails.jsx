import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft, BookOpen, Calendar, Shield, Info, Bell, Copy } from 'lucide-react';
import RequestModal from '../components/RequestModal';

export default function BookDetails() {
  const { bookId } = useParams();
  const navigate = useNavigate();
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    fetchBookDetails();
  }, [bookId]);

  const fetchBookDetails = async () => {
    try {
      const { data } = await axios.get(`/api/books/${bookId}`);
      setBook(data);
    } catch (e) {
      setError(e.response?.data?.error || 'Failed to fetch book details');
    } finally {
      setLoading(false);
    }
  };

  const isAvailable = book?.available_copies > 0;

  if (loading) return (
    <div className="flex justify-center items-center h-64 text-slate-400 animate-pulse">
      <BookOpen className="mr-2" /> Loading details...
    </div>
  );

  if (error || !book) return (
    <div className="text-center py-20">
      <h2 className="text-2xl font-bold text-red-500 mb-4">Oops! Book not found</h2>
      <button onClick={() => navigate('/books')} className="text-primary hover:underline flex items-center justify-center gap-2 mx-auto">
        <ArrowLeft size={16} /> Back to Catalogue
      </button>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      {/* Navigation */}
      <button 
        onClick={() => navigate(-1)} 
        className="mb-6 flex items-center text-slate-500 hover:text-primary transition-colors font-medium group"
      >
        <ArrowLeft className="mr-2 group-hover:-translate-x-1 transition-transform" size={20} />
        Back
      </button>

      <div className="bg-white/90 backdrop-blur-xl rounded-3xl shadow-xl overflow-hidden border border-white/50 relative">
        {/* Background Gradient Decoration */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>

        <div className="flex flex-col md:flex-row">
          {/* Left Column: Cover Image Placeholder */}
          <div className="md:w-1/3 bg-slate-50 p-8 flex items-center justify-center border-r border-slate-100 relative overflow-hidden">
             <div className="aspect-[2/3] w-full max-w-[200px] bg-white rounded-lg shadow-2xl flex flex-col items-center justify-center text-slate-300 relative z-10 border border-slate-100">
                <BookOpen size={64} className="mb-4 text-primary/20" />
                <span className="text-xs uppercase tracking-widest font-semibold text-slate-300">No Cover</span>
             </div>
             {/* Decorative Circles */}
             <div className="absolute inset-0 bg-gradient-to-br from-indigo-50/50 to-purple-50/50 opacity-50"></div>
          </div>

          {/* Right Column: Content */}
          <div className="md:w-2/3 p-8 md:p-10 flex flex-col">
            <div className="flex-1">
              <div className="flex justify-between items-start mb-4">
                <span className="inline-block px-3 py-1 rounded-full text-xs font-bold tracking-wide bg-primary/10 text-primary uppercase">
                  {book.category}
                </span>
                
                <span className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-semibold ${isAvailable ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}`}>
                  {isAvailable ? <Shield size={14} /> : <Info size={14} />}
                  {isAvailable ? 'Available' : 'Out of Stock'}
                </span>
              </div>

              <h1 className="text-3xl md:text-4xl font-extrabold text-slate-800 mb-2 leading-tight">
                {book.title}
              </h1>
              <p className="text-lg text-slate-500 font-medium mb-6">by {book.author}</p>

              {/* Stats Grid */}
              <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="p-4 rounded-xl bg-slate-50/80 border border-slate-100">
                   <div className="text-slate-400 text-xs font-semibold uppercase mb-1 flex items-center gap-1"><Copy size={12}/> Total Copies</div>
                   <div className="text-2xl font-bold text-slate-700">{book.total_copies}</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-50/80 border border-slate-100">
                   <div className="text-slate-400 text-xs font-semibold uppercase mb-1 flex items-center gap-1"><Calendar size={12}/> Added On</div>
                   <div className="text-lg font-semibold text-slate-700">2024</div> {/* Placeholder date */}
                </div>
              </div>

              <div className="prose prose-slate hover:prose-a:text-primary">
                <h3 className="text-lg font-semibold text-slate-800 mb-2">Description</h3>
                <p className="text-slate-600 leading-relaxed">
                  This resource represents a comprehensive guide to <strong>{book.category}</strong>. 
                  It is an essential reading for students in the Computer Department.
                  {/* Since description isn't in DB yet, show generic text */}
                </p>
              </div>
            </div>

            {/* Action Bar */}
            <div className="pt-8 mt-4 border-t border-slate-100 flex gap-4">
               {isAvailable ? (
                 <button disabled className="flex-1 bg-emerald-600/10 text-emerald-700 font-bold py-3.5 px-6 rounded-xl cursor-default flex items-center justify-center gap-2">
                    <Shield size={18} />
                    Available in Library
                 </button>
               ) : (
                 <button 
                    onClick={() => setModalOpen(true)}
                    className="flex-1 bg-gradient-to-r from-primary to-indigo-600 text-white font-bold py-3.5 px-6 rounded-xl shadow-lg shadow-primary/25 hover:shadow-xl hover:shadow-primary/40 hover:-translate-y-0.5 transition-all flex items-center justify-center gap-2"
                 >
                    <Bell size={18} />
                    Notify When Available
                 </button>
               )}
            </div>
          </div>
        </div>
      </div>

      <RequestModal 
        isOpen={modalOpen} 
        onClose={() => setModalOpen(false)} 
        title={`Request Notification: ${book.title}`}
        type="availability_notification"
        defaultDetails={`Please notify me when '${book.title}' by ${book.author} becomes available.`}
      />
    </div>
  );
}
