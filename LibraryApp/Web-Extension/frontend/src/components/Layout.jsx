import { Outlet, Link, useLocation } from 'react-router-dom';
import { LogOut, LayoutDashboard, BookOpen, Clock, FileText, Bell, Search, User, Settings, ScanLine, Menu, X, ChevronLeft, ChevronRight, Home, PanelLeftClose, PanelLeftOpen, Pin, PinOff } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { useState, useEffect, useRef } from 'react';
import Breadcrumbs from './Breadcrumbs';
import AlertBanner from './AlertBanner';

// --- Navigation Configuration ---
const NAV_ITEMS = [
  {
    section: "Main",
    items: [
      { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, path: '/' },
      { id: 'books', label: 'Catalogue', icon: BookOpen, path: '/books' },
      { id: 'profile', label: 'Profile', icon: User, path: '/profile' }
    ]
  },
  {
    section: "Operations",
    items: [
      { id: 'services', label: 'Services', icon: FileText, path: '/services' },
      { id: 'history', label: 'History', icon: Clock, path: '/history' }, // Moved History here
      { id: 'requests', label: 'Requests', icon: Bell, path: '/requests' }
    ]
  },
  {
    section: "Account",
    items: [
      { id: 'settings', label: 'Settings', icon: Settings, path: '/settings' }
    ]
  }
];

export default function Layout({ user, setUser }) {
  const location = useLocation();
  
  // Sidebar State
  const [isPinned, setIsPinned] = useState(true);
  const [isExpanded, setIsExpanded] = useState(true); // Actual visibility state
  
  // Interaction Refs
  const isPointerInSidebar = useRef(false);
  const hoverTimerRef = useRef(null);
  const collapseTimerRef = useRef(null);
  const autoCollapseTimerRef = useRef(null);

  const [profileMenuOpen, setProfileMenuOpen] = useState(false);
  const profileMenuRef = useRef(null);

  const handleLogout = async () => {
    await axios.post('/api/logout');
    setUser(null);
  };

  // --- Interaction Logic ---
  const handleMouseEnterSidebar = () => {
    isPointerInSidebar.current = true;
    if (collapseTimerRef.current) clearTimeout(collapseTimerRef.current);
    if (autoCollapseTimerRef.current) clearTimeout(autoCollapseTimerRef.current);

    if (!isPinned && !isExpanded) {
      hoverTimerRef.current = setTimeout(() => {
        setIsExpanded(true);
      }, 100);
    }
  };

  const handleMouseLeaveSidebar = () => {
    isPointerInSidebar.current = false;
    if (hoverTimerRef.current) clearTimeout(hoverTimerRef.current);

    if (!isPinned) {
      collapseTimerRef.current = setTimeout(() => {
        if (!isPointerInSidebar.current) setIsExpanded(false);
      }, 600);
    }
  };

  const togglePin = () => {
    const newPinned = !isPinned;
    setIsPinned(newPinned);
    if (newPinned) {
      setIsExpanded(true);
      if (collapseTimerRef.current) clearTimeout(collapseTimerRef.current);
      if (autoCollapseTimerRef.current) clearTimeout(autoCollapseTimerRef.current);
    }
  };

  useEffect(() => {
    const handleGlobalMouseMove = (e) => {
      if (isPinned) return;
      const sidebarWidth = 260; 
      const threshold = 60;
      if (e.clientX > (sidebarWidth + threshold)) {
        if (!autoCollapseTimerRef.current && isExpanded && !isPointerInSidebar.current) {
            autoCollapseTimerRef.current = setTimeout(() => {
                if (!isPinned && !isPointerInSidebar.current) setIsExpanded(false);
            }, 400);
        }
      } else {
        if (autoCollapseTimerRef.current) {
            clearTimeout(autoCollapseTimerRef.current);
            autoCollapseTimerRef.current = null;
        }
      }
    };

    if (!isPinned) window.addEventListener('mousemove', handleGlobalMouseMove);
    return () => {
        window.removeEventListener('mousemove', handleGlobalMouseMove);
        if (autoCollapseTimerRef.current) clearTimeout(autoCollapseTimerRef.current);
    };
  }, [isPinned, isExpanded]);

  useEffect(() => {
    return () => {
      if (hoverTimerRef.current) clearTimeout(hoverTimerRef.current);
      if (collapseTimerRef.current) clearTimeout(collapseTimerRef.current);
    };
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target)) {
        setProfileMenuOpen(false);
      }
    };
    if (profileMenuOpen) document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [profileMenuOpen]);

  // --- Render Components ---

  const NavItem = ({ to, icon: Icon, label }) => {
    const isActive = location.pathname === to || (to !== '/' && location.pathname.startsWith(to));
    
    return (
      <Link 
        to={to} 
        title={!isExpanded ? label : ''}
        className={`
          flex items-center gap-3 py-3 rounded-lg transition-colors duration-200 group relative
          ${!isExpanded ? 'justify-center px-2' : 'px-4'}
          ${isActive 
            ? 'bg-brand-blue/10 text-brand-blue font-bold' 
            : 'text-slate-500 hover:bg-slate-100 hover:text-slate-900'}
        `}
      >
        <Icon size={22} className={`shrink-0 transition-colors ${isActive ? 'text-brand-blue' : 'text-slate-400 group-hover:text-slate-600'}`} strokeWidth={isActive ? 2.5 : 2} />
        
        <span className={`nav-label-container transition-all duration-150 ease-out whitespace-nowrap overflow-hidden ${isExpanded ? 'opacity-100 translate-x-0 w-auto' : 'opacity-0 -translate-x-2 w-0'}`}>
          {label}
        </span>
      </Link>
    );
  };

  const MobileTabItem = ({ to, icon: Icon, label }) => {
    const isActive = location.pathname === to || (to !== '/' && location.pathname.startsWith(to));
    return (
      <Link 
        to={to}
        className={`flex flex-col items-center justify-center w-full py-2 transition-colors relative ${
          isActive ? 'text-brand-blue font-bold' : 'text-slate-400 hover:text-slate-600 font-medium'
        }`}
      >
        {isActive && (
           <span className="absolute top-0 w-12 h-0.5 bg-brand-blue rounded-full" />
        )}
        <Icon size={24} className={isActive ? 'fill-current opacity-20' : ''} strokeWidth={isActive ? 2.5 : 2} />
        <span className="text-[10px] mt-1">{label}</span>
      </Link>
    );
  };

  // Dimensions & Classes
  const sidebarClass = isExpanded ? 'sidebar-expanded' : 'sidebar-collapsed';
  // Use margin logic consistent with CSS width
  const mainMargin = isExpanded ? 'ml-0 md:ml-[260px]' : 'ml-0 md:ml-[70px]';

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden isolate relative">
      <div className="fixed top-0 left-0 right-0 z-[60]">
         <AlertBanner />
      </div>
      
      {/* Accessibility: Skip to Content */}
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-24 focus:left-4 focus:z-[100] focus:px-4 focus:py-2 focus:bg-blue-600 focus:text-white focus:rounded-md focus:shadow-lg focus:outline-none">
        Skip to main content
      </a>

      {/* Desktop Sidebar */}
      <aside 
        onMouseEnter={handleMouseEnterSidebar}
        onMouseLeave={handleMouseLeaveSidebar}
        className={`
          hidden md:flex 
          fixed inset-y-0 left-0 z-50
          bg-white border-r border-slate-200 flex-col
          sidebar-transition
          ${sidebarClass}
          ${!isPinned && isExpanded ? 'shadow-2xl shadow-slate-200/50' : ''} 
        `}
      >
        {/* Sidebar Header */}
        <div className={`h-20 flex items-center ${!isExpanded ? 'justify-center' : 'px-6 justify-between'} border-b border-slate-50 shrink-0 sidebar-transition`}>
           <div className="flex items-center gap-3 overflow-hidden">
             <img src="/logo.png" alt="Logo" className="w-8 h-8 object-contain shrink-0" />
             <div className={`whitespace-nowrap transition-all duration-150 ${isExpanded ? 'opacity-100 translate-x-0 w-auto' : 'opacity-0 -translate-x-2 w-0'}`}>
               <h1 className="text-lg font-bold text-slate-800 tracking-tight">GPA's Library</h1>
             </div>
           </div>
           
           <div className={`transition-all duration-150 ${isExpanded ? 'opacity-100 scale-100' : 'opacity-0 scale-0 w-0'}`}>
             <button 
               onClick={togglePin} 
               className={`transition-colors p-1.5 rounded-full hover:bg-slate-100 ${isPinned ? 'text-brand-blue bg-blue-50' : 'text-slate-400 hover:text-slate-600'}`}
               title={isPinned ? "Unpin Sidebar" : "Pin Sidebar"}
             >
               {isPinned ? <Pin size={18} className="fill-current" /> : <PinOff size={18} />}
             </button>
           </div>
        </div>

        {/* Navigation Config Render */}
        <nav className="flex-1 flex flex-col py-6 px-3 gap-1 overflow-y-auto scrollbar-hide" aria-label="Main Navigation">
           {NAV_ITEMS.map((section, idx) => (
             <div key={section.section || idx} className="mb-2" role="group" aria-label={section.section}>
                {/* Section Header */}
                <div className={`px-3 mb-2 transition-all duration-150 overflow-hidden ${isExpanded ? 'opacity-100 max-h-6' : 'opacity-0 max-h-0'}`}>
                   {section.section && <p className="text-xs font-bold text-slate-400 uppercase tracking-wider" id={`heading-${section.section}`}>{section.section}</p>}
                </div>
                
                {/* Items */}
                <div className="space-y-1">
                  {section.items.map(item => (
                    <NavItem key={item.id} to={item.path} icon={item.icon} label={item.label} />
                  ))}
                </div>
                
                {/* Visual Separator if not last */}
                {idx < NAV_ITEMS.length - 1 && isExpanded && <div className="my-4 border-t border-slate-50 mx-3" role="separator"></div>}
             </div>
           ))}
        </nav>

        {/* Sidebar Footer */}
        <div className="p-3 border-t border-slate-100 shrink-0">
           {!isExpanded ? (
             <button onClick={() => setIsExpanded(true)} className="w-full flex justify-center py-3 text-slate-400 hover:text-brand-blue hover:bg-slate-50 rounded-lg transition-colors">
               <PanelLeftOpen size={20} />
             </button>
           ) : (
             <div className="flex items-center justify-between px-3 py-2 bg-slate-50 rounded-xl">
                <div className="flex items-center gap-3 overflow-hidden">
                  <div className="w-8 h-8 rounded-full bg-white border border-slate-200 flex items-center justify-center text-brand-blue font-bold text-xs shrink-0">
                    {user?.name?.charAt(0) || 'U'}
                  </div>
                  <div className="min-w-0">
                     <p className="text-sm font-bold text-slate-700 truncate">{user?.name?.split(' ')[0]}</p>
                     <button onClick={handleLogout} className="text-xs text-red-500 hover:text-red-600 font-medium flex items-center gap-1">
                       <LogOut size={10} /> Logout
                     </button>
                  </div>
                </div>
             </div>
           )}
        </div>
      </aside>

      {/* Main Content */}
      <div className={`flex-1 flex flex-col min-w-0 overflow-hidden relative sidebar-transition ${mainMargin}`}>
        {/* Mobile Header */}
        <header className="h-20 flex items-center justify-between px-4 md:px-10 bg-white/80 backdrop-blur-xl sticky top-0 z-30 border-b border-slate-100">
             <div className="flex items-center gap-4">
                 <div className="w-10 h-10 md:w-12 md:h-12 flex items-center justify-center bg-white rounded-xl shadow-sm border border-slate-100 p-1">
                    <img src="/logo.png" alt="Logo" className="w-full h-full object-contain" />
                 </div>
                 <h1 className="text-lg font-heading font-bold text-slate-900 leading-tight">
                   GPA's Library <br/>
                   <span className="text-xs font-medium text-slate-500 font-sans">Student Portal</span>
                 </h1>
             </div>

             <div className="flex items-center gap-4">
                {/* Desktop Enrollment Pill */}
                <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm font-mono text-slate-600 shadow-sm">
                   <ScanLine size={14} className="text-slate-400" />
                   {user?.enrollment_no || '0000'}
                </div>

                {/* Unified Profile Dropdown */}
                <div className="relative" ref={profileMenuRef}>
                  <button 
                     onClick={() => setProfileMenuOpen(!profileMenuOpen)}
                     className="w-9 h-9 md:w-10 md:h-10 rounded-full bg-slate-100 border border-slate-200 overflow-hidden hover:ring-2 hover:ring-blue-100 transition-all"
                  >
                     <div className="w-full h-full flex items-center justify-center text-slate-500 font-bold text-sm">
                       {user?.name?.charAt(0)}
                     </div>
                  </button>
                  
                  <AnimatePresence>
                    {profileMenuOpen && (
                      <motion.div
                        initial={{ opacity: 0, y: 10, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 10, scale: 0.95 }}
                        transition={{ duration: 0.2, ease: "easeOut" }}
                        className="absolute right-0 top-12 w-48 bg-white rounded-xl shadow-xl shadow-slate-200/50 border border-slate-100 py-1.5 z-50 origin-top-right"
                      >
                        <div className="px-4 py-2 border-b border-slate-50 md:hidden">
                          <p className="text-sm font-bold text-slate-900 truncate">{user?.name}</p>
                          <p className="text-xs text-slate-500 truncate">{user?.enrollment_no}</p>
                        </div>
                        
                        <Link 
                          to="/profile" 
                          onClick={() => setProfileMenuOpen(false)}
                          className="flex items-center gap-2 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
                        >
                          <User size={16} className="text-slate-400"/> Profile
                        </Link>
                        <Link 
                          to="/settings" 
                          onClick={() => setProfileMenuOpen(false)}
                          className="flex items-center gap-2 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
                        >
                          <Settings size={16} className="text-slate-400"/> Settings
                        </Link>
                        <div className="h-px bg-slate-50 my-1"></div>
                        <button 
                          onClick={() => {
                            setProfileMenuOpen(false);
                            handleLogout();
                          }} 
                          className="w-full flex items-center gap-2 px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 text-left transition-colors"
                        >
                          <LogOut size={16}/> Logout
                        </button>
                      </motion.div>
                    )}
                  </AnimatePresence>
               </div>
             </div>
        </header>

        {/* Page Content */}
        <main id="main-content" className="flex-1 overflow-y-auto p-4 md:p-10 pb-24 md:pb-10 scroll-smooth bg-slate-50" tabIndex="-1">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.2 }}
              className="w-full"
            >
              <Outlet />
            </motion.div>
          </AnimatePresence>
        </main>

        {/* Mobile Tab Bar */}
        <div className="md:hidden fixed bottom-6 left-4 right-4 h-16 bg-white/80 backdrop-blur-xl rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.12)] border border-white/20 z-50 flex justify-between items-center px-6 transition-all duration-300">
             <MobileTabItem to="/" icon={Home} label="Home" />
             <MobileTabItem to="/books" icon={BookOpen} label="Books" />
             <MobileTabItem to="/services" icon={FileText} label="Services" />
             <MobileTabItem to="/profile" icon={User} label="Profile" />
        </div>
      </div>
    </div>
  );
}