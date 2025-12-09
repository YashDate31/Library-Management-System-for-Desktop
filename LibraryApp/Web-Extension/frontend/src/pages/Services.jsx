import { useState, useEffect } from 'react';
import axios from 'axios';
import { FileText, Globe, Book, Archive, Download, ExternalLink, Clock } from 'lucide-react';
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
        <h1 className="text-2xl font-bold text-slate-900 mb-2">Services & Notices</h1>
        <p className="text-slate-500">Access digital resources or request library services.</p>
      </div>

      {/* Digital Resources Section */}
      <section>
        <div className="flex items-center justify-between mb-6">
           <h2 className="text-lg font-bold text-slate-800">Digital Library</h2>
        </div>

        {loading ? (
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
             <SkeletonCard />
             <SkeletonCard />
             <SkeletonCard />
           </div>
        ) : error ? (
           <ErrorMessage message={error} onRetry={fetchServices} />
        ) : (
           resources.length === 0 ? (
             <EmptyState
                icon={Archive}
                title="No resources available"
                description="There are currently no digital resources to display. Please check back later."
             />
           ) : (
             <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
               {resources.map((resource) => (
                 <div key={resource.id} className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow group">
                   <div className="flex items-start justify-between mb-4">
                     <div className="p-3 bg-slate-50 rounded-xl group-hover:scale-110 transition-transform">
                        {getIcon(resource.icon)}
                     </div>
                     <span className="bg-slate-100 text-slate-600 text-xs font-bold px-2 py-1 rounded-lg">{resource.type}</span>
                   </div>
                   
                   <h3 className="font-bold text-slate-900 mb-2">{resource.title}</h3>
                   <p className="text-sm text-slate-500 mb-6 leading-relaxed">
                     {resource.description}
                   </p>
                   
                   <a href={resource.link} className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl bg-brand-blue/5 text-brand-blue font-semibold hover:bg-brand-blue/10 transition-colors">
                     Access Now <ExternalLink size={16} />
                   </a>
                 </div>
               ))}
             </div>
           )
        )}
      </section>

      {/* Request Services Section */}
      <section className="pt-8 border-t border-slate-100">
        <h2 className="text-lg font-bold text-slate-800 mb-6">Request Services</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
           <button onClick={() => openRequest('Inter-library Loan')} className="flex items-center gap-4 p-4 bg-white border border-slate-200 rounded-xl hover:border-brand-blue hover:shadow-sm transition-all text-left group">
              <div className="w-10 h-10 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                 <Book size={20} />
              </div>
              <div>
                 <span className="block font-bold text-slate-800">Inter-library Loan</span>
                 <span className="text-xs text-slate-500">Request books from other universities</span>
              </div>
           </button>

           <button onClick={() => openRequest('Study Room Booking')} className="flex items-center gap-4 p-4 bg-white border border-slate-200 rounded-xl hover:border-brand-blue hover:shadow-sm transition-all text-left group">
              <div className="w-10 h-10 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                 <Clock size={20} />
              </div>
              <div>
                 <span className="block font-bold text-slate-800">Study Room Booking</span>
                 <span className="text-xs text-slate-500">Reserve a quiet space for 2 hours</span>
              </div>
           </button>
        </div>
      </section>
    </div>
  );
}
