import { useState, useEffect } from 'react';
import axios from 'axios';
import { Download, RefreshCw, Calendar, Bell, FileText } from 'lucide-react';
import RequestModal from '../components/RequestModal';

export default function Services() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalConfig, setModalConfig] = useState({ title: '', type: '', defaultDetails: '' });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const { data } = await axios.get('/api/dashboard');
      setData(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const openModal = (title, type, defaultDetails) => {
    setModalConfig({ title, type, defaultDetails });
    setModalOpen(true);
  };

  if (loading) return <div className="p-10 text-center text-text-secondary animate-pulse">Loading Services...</div>;

  const notices = data?.notices || [];
  const requests = data?.recent_requests || [];

  return (
    <div className="space-y-8 pb-20">
      
      <RequestModal 
        isOpen={modalOpen} 
        onClose={() => setModalOpen(false)}
        title={modalConfig.title}
        type={modalConfig.type}
        defaultDetails={modalConfig.defaultDetails}
      />

      {/* Page Header */}
      <div>
        <h1 className="text-4xl font-black text-slate-900 mb-2 tracking-tight">Services & Notices</h1>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Left Column - Library Announcements */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-slate-900">Library Announcements</h2>
          
          <div className="space-y-4">
            {/* Announcement 1 */}
            <div className="bg-white rounded-xl p-6 border border-slate-100">
              <h3 className="text-lg font-bold text-slate-900 mb-1">Library Closed on Friday</h3>
              <p className="text-sm text-slate-500 mb-3">Oct 26, 2023</p>
              <p className="text-slate-700 leading-relaxed">
                Please note that the library will be closed this Friday for maintenance. We apologize for any inconvenience.
              </p>
            </div>

            {/* Announcement 2 */}
            <div className="bg-white rounded-xl p-6 border border-slate-100">
              <h3 className="text-lg font-bold text-slate-900 mb-1">New Arrivals in Physics</h3>
              <p className="text-sm text-slate-500 mb-3">Oct 24, 2023</p>
              <p className="text-slate-700 leading-relaxed">
                Explore the latest additions to our physics collection, now available on the 3rd floor.
              </p>
            </div>

            {/* Announcement 3 */}
            <div className="bg-white rounded-xl p-6 border border-slate-100">
              <h3 className="text-lg font-bold text-slate-900 mb-1">Extended Hours for Exams</h3>
              <p className="text-sm text-slate-500 mb-3">Oct 22, 2023</p>
              <p className="text-slate-700 leading-relaxed">
                The library will be open 24/7 during the final exam period, starting next week.
              </p>
            </div>

            {/* Dynamic notices from backend */}
            {notices.map((notice) => (
              <div key={notice.id} className="bg-white rounded-xl p-6 border border-slate-100">
                <h3 className="text-lg font-bold text-slate-900 mb-1">{notice.title}</h3>
                <p className="text-sm text-slate-500 mb-3">{notice.date}</p>
                <p className="text-slate-700 leading-relaxed">{notice.content}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-8">
          
          {/* Self-Service Requests */}
          <div>
            <h2 className="text-2xl font-bold text-slate-900 mb-4">Self-Service Requests</h2>
            
            <div className="flex flex-wrap gap-3">
              <button 
                onClick={() => openModal('Request Renewal', 'renewal', 'I would like to request a renewal for...')}
                className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-bold rounded-lg transition-all active:scale-[0.98] shadow-md shadow-blue-500/20"
              >
                Request Renewal
              </button>
              <button 
                onClick={() => openModal('Request Issue Extension', 'extension', 'I would like to request an extension for...')}
                className="px-6 py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg transition-colors"
              >
                Request Issue Extension
              </button>
              <button 
                onClick={() => openModal('Notify When Available', 'availability_notification', 'Please notify me when the following book becomes available...')}
                className="px-6 py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg transition-colors"
              >
                Notify When Available
              </button>
            </div>
          </div>

          {/* Request Status */}
          <div className="bg-white rounded-xl p-6 border border-slate-100">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-slate-900">Request Status</h2>
              <button 
                onClick={fetchData}
                className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                title="Refresh"
              >
                <RefreshCw size={20} className="text-slate-600" />
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-100">
                    <th className="text-left py-3 px-2 text-sm font-bold text-slate-600 uppercase tracking-wider">Request</th>
                    <th className="text-left py-3 px-2 text-sm font-bold text-slate-600 uppercase tracking-wider">Status</th>
                    <th className="text-left py-3 px-2 text-sm font-bold text-slate-600 uppercase tracking-wider">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {/* Sample requests */}
                  <tr className="border-b border-slate-50">
                    <td className="py-4 px-2 text-slate-900">Renewal: "The Great Gatsby"</td>
                    <td className="py-4 px-2">
                      <span className="inline-block px-3 py-1 bg-yellow-50 text-yellow-700 text-xs font-bold rounded-full">
                        Pending Approval
                      </span>
                    </td>
                    <td className="py-4 px-2 text-slate-600">Oct 25, 2023</td>
                  </tr>
                  <tr className="border-b border-slate-50">
                    <td className="py-4 px-2 text-slate-900">Extension: "Cosmos"</td>
                    <td className="py-4 px-2">
                      <span className="inline-block px-3 py-1 bg-green-50 text-green-700 text-xs font-bold rounded-full">
                        Approved
                      </span>
                    </td>
                    <td className="py-4 px-2 text-slate-600">Oct 23, 2023</td>
                  </tr>
                  <tr className="border-b border-slate-50">
                    <td className="py-4 px-2 text-slate-900">Notify: "Dune Messiah"</td>
                    <td className="py-4 px-2">
                      <span className="inline-block px-3 py-1 bg-red-50 text-red-700 text-xs font-bold rounded-full">
                        Rejected
                      </span>
                    </td>
                    <td className="py-4 px-2 text-slate-600">Oct 20, 2023</td>
                  </tr>

                  {/* Dynamic requests from backend */}
                  {requests.slice(0, 3).map((req, index) => (
                    <tr key={index} className="border-b border-slate-50">
                      <td className="py-4 px-2 text-slate-900">{req.request_type}: {req.details}</td>
                      <td className="py-4 px-2">
                        <span className={`inline-block px-3 py-1 text-xs font-bold rounded-full ${
                          req.status === 'pending' ? 'bg-yellow-50 text-yellow-700' :
                          req.status === 'approved' ? 'bg-green-50 text-green-700' :
                          'bg-red-50 text-red-700'
                        }`}>
                          {req.status.charAt(0).toUpperCase() + req.status.slice(1)}
                        </span>
                      </td>
                      <td className="py-4 px-2 text-slate-600">{new Date(req.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Digital Documents */}
          <div className="bg-white rounded-xl p-6 border border-slate-100">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">Digital Documents</h2>
            
            <div className="space-y-3">
              <DocumentRow title="Overdue Warning Letter.pdf" />
              <DocumentRow title="No Dues Certificate.pdf" />
              <DocumentRow title="Library Membership Card.pdf" />
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

function DocumentRow({ title }) {
  return (
    <div className="flex items-center justify-between py-3 px-4 hover:bg-slate-50 rounded-lg transition-colors group">
      <div className="flex items-center gap-3">
        <FileText className="text-slate-400" size={20} />
        <span className="text-slate-900 font-medium">{title}</span>
      </div>
      <button 
        onClick={() => alert(`Downloading ${title}...`)}
        className="p-2 text-blue-500 hover:bg-blue-50 rounded-lg transition-colors"
        title="Download"
      >
        <Download size={18} />
      </button>
    </div>
  );
}
