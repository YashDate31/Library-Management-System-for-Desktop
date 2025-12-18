import { useState, useEffect } from 'react';
import axios from 'axios';
import { FileText, Book, Clock, DoorOpen, GraduationCap, Send } from 'lucide-react';
import RequestModal from '../components/RequestModal';
import Skeleton, { SkeletonCard } from '../components/ui/Skeleton';
import ErrorMessage from '../components/ui/ErrorMessage';
import EmptyState from '../components/ui/EmptyState';

export default function Services() {
  const [modalOpen, setModalOpen] = useState(false);
  const [requestType, setRequestType] = useState('');
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    try {
      const { data } = await axios.get('/api/services');
      setResources(data.resources);
    } catch (e) {
      console.error("Failed to load services", e);
      setError("Could not load digital resources.");
    } finally {
      setLoading(false);
    }
  };

  const openRequest = (type) => {
    setRequestType(type);
    setModalOpen(true);
  };

  const getIcon = (iconName) => {
    switch (iconName) {
      case 'Globe': return <Globe className="text-blue-500" size={24} />;
      case 'Book': return <Book className="text-purple-500" size={24} />;
      case 'Archive': return <Archive className="text-amber-500" size={24} />;
      default: return <FileText className="text-slate-500" size={24} />;
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-10 font-sans">
      <RequestModal 
        isOpen={modalOpen} 
        onClose={() => setModalOpen(false)}
        title={`Request: ${requestType}`}
        type={requestType}
      />
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 mb-2">Library Services</h1>
        <p className="text-slate-500">Submit requests for library services and permissions.</p>
      </div>

      {/* Request Services Section */}
      <section>
        <h2 className="text-lg font-bold text-slate-800 mb-6">Available Services</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
           {/* Request a Book */}
           <button onClick={() => openRequest('Book Request')} className="flex items-center gap-4 p-5 bg-white border border-slate-200 rounded-xl hover:border-brand-blue hover:shadow-md transition-all text-left group">
              <div className="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                 <Book size={22} />
              </div>
              <div>
                 <span className="block font-bold text-slate-800">Request a Book</span>
                 <span className="text-xs text-slate-500">Request new books for the library</span>
              </div>
           </button>

           {/* 2 Hour Permission */}
           <button onClick={() => openRequest('Extended Hours Permission')} className="flex items-center gap-4 p-5 bg-white border border-slate-200 rounded-xl hover:border-brand-blue hover:shadow-md transition-all text-left group">
              <div className="w-12 h-12 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                 <Clock size={22} />
              </div>
              <div>
                 <span className="block font-bold text-slate-800">2 Hour Permission</span>
                 <span className="text-xs text-slate-500">Request extended library access</span>
              </div>
           </button>

           {/* Library Opening Request */}
           <button onClick={() => openRequest('Library Opening Request')} className="flex items-center gap-4 p-5 bg-white border border-slate-200 rounded-xl hover:border-brand-blue hover:shadow-md transition-all text-left group">
              <div className="w-12 h-12 rounded-full bg-amber-50 flex items-center justify-center text-amber-600 group-hover:bg-amber-600 group-hover:text-white transition-colors">
                 <DoorOpen size={22} />
              </div>
              <div>
                 <span className="block font-bold text-slate-800">Library Opening Request</span>
                 <span className="text-xs text-slate-500">Request library to open outside hours</span>
              </div>
           </button>

           {/* Study Materials Request */}
           <button onClick={() => openRequest('Study Materials Request')} className="flex items-center gap-4 p-5 bg-white border border-slate-200 rounded-xl hover:border-brand-blue hover:shadow-md transition-all text-left group">
              <div className="w-12 h-12 rounded-full bg-purple-50 flex items-center justify-center text-purple-600 group-hover:bg-purple-600 group-hover:text-white transition-colors">
                 <GraduationCap size={22} />
              </div>
              <div>
                 <span className="block font-bold text-slate-800">Request Study Materials</span>
                 <span className="text-xs text-slate-500">Ask for specific study resources</span>
              </div>
           </button>

           {/* General Request */}
           <button onClick={() => openRequest('General Request')} className="flex items-center gap-4 p-5 bg-white border border-slate-200 rounded-xl hover:border-brand-blue hover:shadow-md transition-all text-left group sm:col-span-2">
              <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 group-hover:bg-slate-600 group-hover:text-white transition-colors">
                 <Send size={22} />
              </div>
              <div>
                 <span className="block font-bold text-slate-800">Other Request</span>
                 <span className="text-xs text-slate-500">Submit any other library-related request</span>
              </div>
           </button>
        </div>
      </section>
    </div>
  );
}
