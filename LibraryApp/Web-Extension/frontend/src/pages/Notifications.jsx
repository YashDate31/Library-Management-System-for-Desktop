import { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Bell, Check, Trash2, AlertTriangle, Info, Megaphone, Clock, CheckCircle2, X } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import EmptyState from '../components/ui/EmptyState';

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all'); // all, alerts, updates, announcements
  const navigate = useNavigate();

  const formatTime = (dateStr) => {
    if (!dateStr) return '';
    try {
        const date = new Date(dateStr);
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);
        
        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
        if (diffInSeconds < 172800) return 'Yesterday';
        return date.toLocaleDateString();
    } catch (e) {
        return dateStr?.split(' ')[0] || '';
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      const { data } = await axios.get('/api/notifications');
      setNotifications(data.notifications || []);
    } catch (e) {
      console.error("Failed to fetch notifications", e);
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAllRead = async () => {
    try {
        await axios.post('/api/notifications/mark-read', { id: 'all' });
        // Optimistic update
        setNotifications(prev => prev.map(n => ({ ...n, is_read: 1 })));
    } catch (e) {
        console.error("Failed to mark all read", e);
    }
  };

  const handleMarkRead = async (id, e) => {
      e.stopPropagation();
      try {
          await axios.post('/api/notifications/mark-read', { id });
           setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: 1 } : n));
      } catch (e) {
          console.error("Failed to mark read", e);
      }
  };

  const handleDelete = async (id, e) => {
      e.stopPropagation();
      if (!window.confirm("Delete this notification?")) return;
      try {
          await axios.delete(`/api/notifications/${id}`);
          setNotifications(prev => prev.filter(n => n.id !== id));
      } catch (e) {
          console.error("Failed to delete", e);
      }
  };

  // Filter Logic
  const filtered = notifications.filter(n => {
      if (activeTab === 'all') return true;
      if (activeTab === 'alerts') return n.type === 'danger' || n.type === 'warning';
      if (activeTab === 'updates') return n.type === 'request_update';
      if (activeTab === 'announcements') return n.type === 'system';
      return true;
  });

  const getIcon = (type) => {
      switch(type) {
          case 'danger': return <AlertTriangle className="text-red-500" />;
          case 'warning': return <Clock className="text-amber-500" />;
          case 'request_update': return <CheckCircle2 className="text-blue-500" />;
          case 'system': return <Megaphone className="text-purple-500" />;
          default: return <Info className="text-slate-500" />;
      }
  };

  const getBgColor = (type, isRead) => {
      if (isRead) return 'bg-white dark:bg-slate-900 border-slate-100 dark:border-slate-800 opacity-60';
      switch(type) {
          case 'danger': return 'bg-red-50 dark:bg-red-900/10 border-red-100 dark:border-red-900/30';
          case 'warning': return 'bg-amber-50 dark:bg-amber-900/10 border-amber-100 dark:border-amber-900/30';
          case 'request_update': return 'bg-blue-50 dark:bg-blue-900/10 border-blue-100 dark:border-blue-900/30';
          case 'system': return 'bg-purple-50 dark:bg-purple-900/10 border-purple-100 dark:border-purple-900/30';
          default: return 'bg-white dark:bg-slate-900 border-slate-100 dark:border-slate-800';
      }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 pb-20">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
            <div>
                <h1 className="text-3xl font-black text-slate-900 dark:text-white tracking-tight flex items-center gap-3">
                    <Bell className="text-blue-600 dark:text-blue-400" size={32} /> 
                    Notifications
                </h1>
                <p className="text-slate-500 dark:text-slate-400 mt-1">Stay updated with your library activity.</p>
            </div>
            <div className="flex gap-2">
                <Button variant="secondary" size="sm" onClick={handleMarkAllRead}>
                    <Check size={16} className="mr-2" /> Mark all read
                </Button>
            </div>
        </div>

        {/* Tabs */}
        <div className="flex overflow-x-auto pb-4 mb-4 gap-2 scrollbar-hide">
            {['all', 'alerts', 'updates', 'announcements'].map(tab => (
                <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`
                        px-4 py-2 rounded-full text-sm font-bold capitalize whitespace-nowrap transition-all
                        ${activeTab === tab 
                            ? 'bg-slate-900 dark:bg-white text-white dark:text-slate-900 shadow-md transform scale-105' 
                            : 'bg-white dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700'}
                    `}
                >
                    {tab}
                </button>
            ))}
        </div>

        {/* Notification List */}
        <div className="space-y-3 min-h-[300px]">
            {loading ? (
                <div className="space-y-4">
                    {[1,2,3].map(i => <div key={i} className="h-24 bg-slate-100 dark:bg-slate-800 rounded-2xl animate-pulse"/>)}
                </div>
            ) : filtered.length === 0 ? (
                <EmptyState 
                    icon={Bell} 
                    title="All caught up!" 
                    description="You have no notifications in this category."
                />
            ) : (
                <AnimatePresence mode="popLayout">
                    {filtered.map(notif => (
                        <motion.div
                            key={notif.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            layout
                            onClick={() => notif.link && navigate(notif.link)}
                            className={`
                                relative p-5 rounded-2xl border transition-all duration-300 group
                                ${getBgColor(notif.type, notif.is_read)}
                                ${notif.link ? 'cursor-pointer hover:shadow-md' : ''}
                            `}
                        >
                            <div className="flex items-start gap-4">
                                <div className={`p-3 rounded-full bg-white dark:bg-slate-800 shrink-0 shadow-sm ${notif.is_read ? 'grayscale opacity-50' : ''}`}>
                                    {getIcon(notif.type)}
                                </div>
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center justify-between mb-1">
                                        <h3 className={`font-bold text-lg ${notif.is_read ? 'text-slate-600 dark:text-slate-500' : 'text-slate-900 dark:text-white'}`}>
                                            {notif.title}
                                        </h3>
                                        <span className="text-xs font-medium text-slate-400 dark:text-slate-500 whitespace-nowrap ml-2">
                                            {formatTime(notif.created_at)}
                                        </span>
                                    </div>
                                    <p className={`text-sm leading-relaxed ${notif.is_read ? 'text-slate-500 dark:text-slate-600' : 'text-slate-700 dark:text-slate-300'}`}>
                                        {notif.message}
                                    </p>
                                </div>
                            </div>
                            
                            {/* Actions Overlay (Desktop) */}
                            <div className="absolute top-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                {!notif.is_read && (
                                    <button 
                                        onClick={(e) => handleMarkRead(notif.id, e)}
                                        className="p-2 bg-white dark:bg-slate-800 text-slate-400 hover:text-blue-500 rounded-lg shadow-sm border border-slate-100 dark:border-slate-700 transition"
                                        title="Mark as read"
                                    >
                                        <Check size={16} />
                                    </button>
                                )}
                                {typeof notif.id === 'number' && ( // Only DB items can be deleted
                                    <button 
                                        onClick={(e) => handleDelete(notif.id, e)}
                                        className="p-2 bg-white dark:bg-slate-800 text-slate-400 hover:text-red-500 rounded-lg shadow-sm border border-slate-100 dark:border-slate-700 transition"
                                        title="Delete"
                                    >
                                        <Trash2 size={16} />
                                    </button>
                                )}
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
            )}
        </div>
    </div>
  );
}
