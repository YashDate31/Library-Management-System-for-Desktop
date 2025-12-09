import { useState, useEffect } from 'react';
import axios from 'axios';
import { CheckCircle, AlertTriangle, Award, BookOpen, DollarSign, Calendar } from 'lucide-react';

export default function History() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
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

  if (loading) return <div className="p-10 text-center text-text-secondary animate-pulse">Loading History...</div>;
  if (!data) return <div className="p-10 text-center text-text-secondary">No data available</div>;

  const { history = [], analytics } = data;
  const { stats = {}, badges = [] } = analytics || {};

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
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Left Column - Reading History */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-slate-900">Reading History</h2>
          
          <div className="space-y-3">
            {history.slice(0, 10).map((book, index) => {
              const returnDate = book.return_date ? new Date(book.return_date).toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' }) : 'N/A';
              const isLate = book.status === 'overdue' || (book.borrow_date && book.return_date && new Date(book.return_date) > new Date(book.borrow_date));
              
              return (
                <div key={index} className="bg-white rounded-xl p-5 border border-slate-100 hover:shadow-md transition-shadow">
                  <div className="flex items-start gap-4">
                    {/* Status Icon */}
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${isLate ? 'bg-red-50' : 'bg-green-50'}`}>
                      {isLate ? (
                        <AlertTriangle className="text-red-500" size={20} />
                      ) : (
                        <CheckCircle className="text-green-500" size={20} />
                      )}
                    </div>

                    {/* Book Info */}
                    <div className="flex-1">
                      <h3 className="font-bold text-slate-900 text-lg leading-tight mb-1">{book.title}</h3>
                      <p className="text-slate-500 text-sm mb-2">Returned: {returnDate}</p>
                      <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold ${
                        isLate 
                          ? 'bg-red-50 text-red-600' 
                          : 'bg-green-50 text-green-600'
                      }`}>
                        {isLate ? 'Returned Late - Fine Paid' : 'Returned on Time'}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column - Stats & Fun */}
        <div className="space-y-8">
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
              <p className="text-4xl font-black text-slate-900">${stats.total_fines || 0}.00</p>
            </div>

            {/* Academic Year */}
            <div className="bg-white rounded-xl p-5 border border-slate-100 text-center">
              <p className="text-slate-600 font-medium text-sm mb-2">Academic Year</p>
              <p className="text-4xl font-black text-slate-900">3rd</p>
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
