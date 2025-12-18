import { useState, useEffect } from 'react';
import axios from 'axios';
import { Download, FileText, BookOpen, Calendar, Filter } from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Skeleton from '../components/ui/Skeleton';
import ErrorMessage from '../components/ui/ErrorMessage';
import EmptyState from '../components/ui/EmptyState';

export default function StudyMaterials({ user }) {
  const [materials, setMaterials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [yearFilter, setYearFilter] = useState('All');

  useEffect(() => {
    fetchMaterials();
  }, [yearFilter]);

  const fetchMaterials = async () => {
    try {
      setLoading(true);
      const params = yearFilter !== 'All' ? { year: yearFilter } : {};
      const { data } = await axios.get('/api/study-materials', { params });
      setMaterials(data.materials || []);
      setError(null);
    } catch (e) {
      console.error("Failed to fetch materials", e);
      setError("Could not load study materials");
    } finally {
      setLoading(false);
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'Notes': return '📝';
      case 'PYQ': return '📄';
      case 'Syllabus': return '📋';
      default: return '📚';
    }
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'Notes': return 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300';
      case 'PYQ': return 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300';
      case 'Syllabus': return 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300';
      default: return 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300';
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return 'Recently';
    try {
      return new Date(dateStr).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
    } catch (e) {
      return dateStr;
    }
  };

  if (loading) return <MaterialsSkeleton />;
  if (error) return (
    <div className="p-6">
      <ErrorMessage message={error} onRetry={fetchMaterials} />
    </div>
  );

  return (
    <div className="min-h-screen bg-slate-50/50 dark:bg-slate-950 pb-24 md:pb-10 transition-colors">
      <div className="px-4 py-6 space-y-6 max-w-6xl mx-auto">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">
              📚 Study Materials
            </h1>
            <p className="text-slate-500 dark:text-slate-400 mt-1">
              Access notes, previous year questions, and study resources
            </p>
          </div>

          {/* Year Filter */}
          <div className="flex items-center gap-3">
            <Filter className="w-5 h-5 text-slate-400" />
            <select
              value={yearFilter}
              onChange={(e) => setYearFilter(e.target.value)}
              className="px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-white font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="All">All Years</option>
              <option value="1st">1st Year</option>
              <option value="2nd">2nd Year</option>
              <option value="3rd">3rd Year</option>
            </select>
          </div>
        </div>

        {/* Materials Grid */}
        {materials.length === 0 ? (
          <EmptyState
            icon={BookOpen}
            title="No materials available"
            description={yearFilter === 'All' ? "No study materials have been uploaded yet." : `No materials for ${yearFilter} year.`}
            actionLabel="Refresh"
            onAction={fetchMaterials}
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {materials.map((material) => (
              <Card key={material.id} className="group hover:shadow-lg transition-all duration-300 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                <div className="p-6">
                  {/* Category Badge */}
                  <div className="flex items-center justify-between mb-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${getCategoryColor(material.category)}`}>
                      {getCategoryIcon(material.category)} {material.category || 'Material'}
                    </span>
                    <span className="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase">
                      {material.year}
                    </span>
                  </div>

                  {/* Title */}
                  <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2 line-clamp-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    {material.title}
                  </h3>

                  {/* Description */}
                  {material.description && (
                    <p className="text-sm text-slate-600 dark:text-slate-400 mb-4 line-clamp-2">
                      {material.description}
                    </p>
                  )}

                  {/* Footer */}
                  <div className="flex items-center justify-between pt-4 border-t border-slate-100 dark:border-slate-800">
                    <div className="flex items-center gap-2 text-xs text-slate-400 dark:text-slate-500">
                      <Calendar size={14} />
                      <span>{formatDate(material.upload_date)}</span>
                    </div>

                    <a
                      href={material.drive_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold rounded-lg transition-all shadow-sm hover:shadow-md active:scale-95"
                    >
                      <Download size={16} />
                      Download
                    </a>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Info Banner */}
        <Card className="bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800">
          <div className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-100 dark:bg-blue-800/50 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center shrink-0">
              <FileText size={20} />
            </div>
            <div className="flex-1">
              <h4 className="font-bold text-blue-900 dark:text-blue-100 text-sm">Download Study Materials</h4>
              <p className="text-xs text-blue-700 dark:text-blue-300 mt-0.5">
                All materials are hosted on Google Drive. Click "Download" to access them directly.
              </p>
            </div>
          </div>
        </Card>

      </div>
    </div>
  );
}

function MaterialsSkeleton() {
  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto">
      <Skeleton className="h-10 w-64" />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3, 4, 5, 6].map(i => (
          <Skeleton key={i} className="h-56 w-full rounded-2xl" />
        ))}
      </div>
    </div>
  );
}
