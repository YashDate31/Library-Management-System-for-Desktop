import { useState, useEffect } from 'react';
import axios from 'axios';
import { CheckCircle, AlertTriangle, Award, BookOpen, DollarSign, Calendar, History as HistoryIcon, XCircle, Clock } from 'lucide-react';
import EmptyState from '../components/ui/EmptyState';
import { Link } from 'react-router-dom';

export default function History({ user }) {
  const [data, setData] = useState(null);
  const [loanHistory, setLoanHistory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all'); // all, borrowed, overdue, on-time, late

  useEffect(() => {
    fetchHistory();
    fetchLoanHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const { data } = await axios.get('/api/dashboard');
      setData(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const fetchLoanHistory = async () => {
    try {
      const { data } = await axios.get('/api/loan-history');
      setLoanHistory(data);
    } catch (e) {
      console.error(e);
    }
  };

  if (loading) return <div className="p-10 text-center text-slate-500 animate-pulse font-medium">Loading History...</div>;
  if (!data || (!data.history || data.history.length === 0) && (!loanHistory || loanHistory.total_borrowed === 0)) return (
     <div className="p-10">
        <EmptyState 
           icon={HistoryIcon}
           title="No reading history yet"
           description="You haven't borrowed any books yet. Once you start reading, your history and stats will appear here."
           actionLabel="Start Reading"
           onAction={() => window.location.href = '/books'}
        />
     </div>
  );

  const { history = [], analytics } = data;
  const { stats = {}, badges = [] } = analytics || {};

  // Get all loan records
  const allLoans = [];
  if (loanHistory) {
    if (activeTab === 'all' || activeTab === 'borrowed') allLoans.push(...(loanHistory.currently_borrowed || []));
    if (activeTab === 'all' || activeTab === 'overdue') allLoans.push(...(loanHistory.currently_overdue || []));
    if (activeTab === 'all' || activeTab === 'on-time') allLoans.push(...(loanHistory.returned_on_time || []));
    if (activeTab === 'all' || activeTab === 'late') allLoans.push(...(loanHistory.returned_late || []));
  }

  // Calculate reading preferences from category distribution
  const categoryData = stats.categories || {};
  const totalBooks = Object.values(categoryData).reduce((sum, count) => sum + count, 0);
  const categoryPercentages = Object.entries(categoryData).map(([name, count]) => ({
    name,
    percentage: totalBooks > 0 ? Math.round((count / totalBooks) * 100) : 0,
    count
  })).sort((a, b) => b.percentage - a.percentage);

  const topCategory = categoryPercentages[0] || { name: 'N/A', percentage: 0 };
  const secondCategory = categoryPercentages[1] || { name: 'N/A', percentage: 0 };

  return (
    <div className="space-y-8 pb-20">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-black text-slate-900 mb-2 tracking-tight">My Library Journey</h1>
        <p className="text-slate-600">Complete history of all your borrowed books</p>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        <button
          onClick={() => setActiveTab('all')}
          className={`px-4 py-2 rounded-xl font-semibold text-sm whitespace-nowrap transition-all ${
            activeTab === 'all' ? 'bg-blue-600 text-white shadow-md' : 'bg-white text-slate-600 border border-slate-200 hover:border-blue-300'
          }`}
        >
          All ({loanHistory?.total_borrowed || 0})
        </button>
        <button
          onClick={() => setActiveTab('borrowed')}
          className={`px-4 py-2 rounded-xl font-semibold text-sm whitespace-nowrap transition-all ${
            activeTab === 'borrowed' ? 'bg-green-600 text-white shadow-md' : 'bg-white text-slate-600 border border-slate-200 hover:border-green-300'
          }`}
        >
          Currently Borrowed ({loanHistory?.currently_borrowed?.length || 0})
        </button>
        <button
          onClick={() => setActiveTab('overdue')}
          className={`px-4 py-2 rounded-xl font-semibold text-sm whitespace-nowrap transition-all ${
            activeTab === 'overdue' ? 'bg-red-600 text-white shadow-md' : 'bg-white text-slate-600 border border-slate-200 hover:border-red-300'
          }`}
        >
          Currently Overdue ({loanHistory?.currently_overdue?.length || 0})
        </button>
        <button
          onClick={() => setActiveTab('on-time')}
          className={`px-4 py-2 rounded-xl font-semibold text-sm whitespace-nowrap transition-all ${
            activeTab === 'on-time' ? 'bg-emerald-600 text-white shadow-md' : 'bg-white text-slate-600 border border-slate-200 hover:border-emerald-300'
          }`}
        >
          Returned On Time ({loanHistory?.returned_on_time?.length || 0})
        </button>
        <button
          onClick={() => setActiveTab('late')}
          className={`px-4 py-2 rounded-xl font-semibold text-sm whitespace-nowrap transition-all ${
            activeTab === 'late' ? 'bg-orange-600 text-white shadow-md' : 'bg-white text-slate-600 border border-slate-200 hover:border-orange-300'
          }`}
        >
          Returned Late ({loanHistory?.returned_late?.length || 0})
        </button>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column - Loan History (2 columns wide) */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-2xl font-bold text-slate-900">
            {activeTab === 'all' && 'All Loan Records'}
            {activeTab === 'borrowed' && 'Currently Borrowed'}
            {activeTab === 'overdue' && 'Currently Overdue'}
            {activeTab === 'on-time' && 'Returned On Time'}
            {activeTab === 'late' && 'Returned Late'}
          </h2>
          
          <div className="space-y-3">
            {allLoans.length === 0 ? (
              <div className="bg-white rounded-xl p-10 border border-slate-100 text-center">
                <p className="text-slate-500">No records in this category</p>
              </div>
            ) : (
              allLoans.map((record, index) => {
                const getStatusInfo = () => {
                  if (record.actual_status === 'Currently Borrowed') {
                    return { icon: Clock, color: 'bg-blue-50', textColor: 'text-blue-600', iconColor: 'text-blue-500' };
                  } else if (record.actual_status === 'Currently Overdue') {
                    return { icon: AlertTriangle, color: 'bg-red-50', textColor: 'text-red-600', iconColor: 'text-red-500' };
                  } else if (record.actual_status === 'Returned On Time') {
                    return { icon: CheckCircle, color: 'bg-green-50', textColor: 'text-green-600', iconColor: 'text-green-500' };
                  } else {
                    return { icon: XCircle, color: 'bg-orange-50', textColor: 'text-orange-600', iconColor: 'text-orange-500' };
                  }
                };
                
                const statusInfo = getStatusInfo();
                const StatusIcon = statusInfo.icon;
                
                return (
                  <div key={index} className="bg-white rounded-xl p-5 border border-slate-100 hover:shadow-md transition-shadow">
                    <div className="flex items-start gap-4">
                      <div className={`w-12 h-12 rounded-full flex items-center justify-center shrink-0 ${statusInfo.color}`}>
                        <StatusIcon className={statusInfo.iconColor} size={22} />
                      </div>

                      <div className="flex-1">
                        <h3 className="font-bold text-slate-900 text-lg leading-tight mb-1">{record.title}</h3>
                        <p className="text-slate-500 text-sm mb-2">by {record.author} • {record.category}</p>
                        
                        <div className="flex flex-wrap gap-2 mb-3 text-xs text-slate-600">
                          <span>Borrowed: {new Date(record.borrow_date).toLocaleDateString()}</span>
                          {record.due_date && <span>• Due: {new Date(record.due_date).toLocaleDateString()}</span>}
                          {record.return_date && <span>• Returned: {new Date(record.return_date).toLocaleDateString()}</span>}
                        </div>
                        
                        <div className="flex items-center gap-2">
                          <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold ${statusInfo.color} ${statusInfo.textColor}`}>
                            {record.actual_status}
                          </span>
                          
                          {record.overdue_days > 0 && (
                            <span className="inline-block px-3 py-1 rounded-full text-xs font-bold bg-red-100 text-red-700">
                              {record.overdue_days} days overdue
                            </span>
                          )}
                          
                          {record.days_left >= 0 && (
                            <span className="inline-block px-3 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-700">
                              {record.days_left} days left
                            </span>
                          )}
                          
                          {record.fine_paid && (
                            <span className="inline-block px-3 py-1 rounded-full text-xs font-bold bg-green-100 text-green-700">
                              Fine Paid: ₹{record.fine || 0}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right Column - Stats & Fun */}
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-slate-900">Stats & Fun</h2>

          {/* Stats Cards */}
          <div className="grid grid-cols-3 gap-4">
            {/* Total Books Read */}
            <div className="bg-white rounded-xl p-5 border border-slate-100 text-center">
              <p className="text-slate-600 font-medium text-sm mb-2">Total Books Read</p>
              <p className="text-4xl font-black text-slate-900">{stats.total_books || 0}</p>
            </div>

            {/* Total Fines Paid */}
            <div className="bg-white rounded-xl p-5 border border-slate-100 text-center">
              <p className="text-slate-600 font-medium text-sm mb-2">Total Fines Paid</p>
              <p className="text-4xl font-black text-slate-900">{stats.total_fines || 0}</p>
            </div>

            {/* Academic Year */}
            <div className="bg-white rounded-xl p-5 border border-slate-100 text-center">
              <p className="text-slate-600 font-medium text-sm mb-2">Academic Year</p>
              <p className="text-4xl font-black text-slate-900">{user?.year || 'N/A'}</p>
            </div>
          </div>

          {/* Reading Preferences */}
          <div className="bg-white rounded-xl p-6 border border-slate-100">
            <h3 className="text-xl font-bold text-slate-900 mb-6">Reading Preferences</h3>
            
            <div className="flex items-center gap-8">
              {/* Donut Chart */}
              <div className="relative w-40 h-40 shrink-0">
                <svg viewBox="0 0 100 100" className="transform -rotate-90">
                  {/* Background circle */}
                  <circle
                    cx="50"
                    cy="50"
                    r="40"
                    fill="none"
                    stroke="#e2e8f0"
                    strokeWidth="12"
                  />
                  {/* Top category segment */}
                  <circle
                    cx="50"
                    cy="50"
                    r="40"
                    fill="none"
                    stroke="#3b82f6"
                    strokeWidth="12"
                    strokeDasharray={`${topCategory.percentage * 2.51} ${251 - topCategory.percentage * 2.51}`}
                    strokeLinecap="round"
                  />
                  {/* Second category segment */}
                  {secondCategory.percentage > 0 && (
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      fill="none"
                      stroke="#93c5fd"
                      strokeWidth="12"
                      strokeDasharray={`${secondCategory.percentage * 2.51} ${251 - secondCategory.percentage * 2.51}`}
                      strokeDashoffset={-topCategory.percentage * 2.51}
                      strokeLinecap="round"
                    />
                  )}
                </svg>
                {/* Center text */}
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <p className="text-3xl font-black text-slate-900">{topCategory.percentage}%</p>
                  <p className="text-xs text-slate-500 font-medium">{topCategory.name}</p>
                </div>
              </div>

              {/* Legend */}
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                  <span className="text-sm font-medium text-slate-700">{topCategory.percentage}% {topCategory.name}</span>
                </div>
                {secondCategory.percentage > 0 && (
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 rounded-full bg-blue-300"></div>
                    <span className="text-sm font-medium text-slate-700">{secondCategory.percentage}% {secondCategory.name}</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Trophy Case */}
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-slate-900">Trophy Case</h3>
            
            <div className="grid grid-cols-3 gap-4">
              {badges.map((badge, index) => (
                <div key={index} className="bg-white rounded-xl p-4 border border-slate-100 text-center hover:shadow-md transition-shadow">
                  <div className="text-4xl mb-2">{badge.icon}</div>
                  <p className="text-sm font-bold text-slate-900">{badge.label}</p>
                </div>
              ))}
              
              {/* Placeholder badges if none exist */}
              {badges.length === 0 && (
                <>
                  <div className="bg-white rounded-xl p-4 border border-slate-100 text-center">
                    <div className="w-12 h-12 rounded-full bg-yellow-50 flex items-center justify-center mx-auto mb-2">
                      <Award className="text-yellow-500" size={24} />
                    </div>
                    <p className="text-sm font-bold text-slate-900">Java Master</p>
                  </div>
                  <div className="bg-white rounded-xl p-4 border border-slate-100 text-center">
                    <div className="w-12 h-12 rounded-full bg-green-50 flex items-center justify-center mx-auto mb-2">
                      <CheckCircle className="text-green-500" size={24} />
                    </div>
                    <p className="text-sm font-bold text-slate-900">Zero Overdue Legend</p>
                  </div>
                  <div className="bg-white rounded-xl p-4 border border-slate-100 text-center">
                    <div className="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center mx-auto mb-2">
                      <BookOpen className="text-blue-500" size={24} />
                    </div>
                    <p className="text-sm font-bold text-slate-900">Active Reader</p>
                  </div>
                </>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
