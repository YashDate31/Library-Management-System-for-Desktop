import { Outlet, Link, useLocation } from 'react-router-dom';
import { LogOut, LayoutDashboard, BookOpen, Clock, FileText, Bell, Search, User, Settings, ScanLine, Menu, X, ChevronLeft, ChevronRight, Home } from 'lucide-react';
import axios from 'axios';
import { useState, useEffect, useRef } from 'react';
import Breadcrumbs from './Breadcrumbs';
import AlertBanner from './AlertBanner';

export default function Layout({ user, setUser }) {
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false); // Mobile only (Legacy state, keeping for safety, but main nav is now bottom tabs)
  const [isExpanded, setIsExpanded] = useState(false); // Desktop hover state
  
  // Three modes: 'expanded', 'collapsed', 'hover'
  const [sidebarMode, setSidebarMode] = useState('hover');
  const [menuOpen, setMenuOpen] = useState(false);
  
  // Refs for debouncing
  const enterTimeoutRef = useRef(null);
  const leaveTimeoutRef = useRef(null);
  const menuRef = useRef(null);
  const profileMenuRef = useRef(null);

  const [profileMenuOpen, setProfileMenuOpen] = useState(false);

  const handleLogout = async () => {
    await axios.post('/api/logout');
    setUser(null);
  };

  const closeSidebar = () => setSidebarOpen(false);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target)) {
        setProfileMenuOpen(false);
      }
    };

    if (menuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [menuOpen]);

  // Desktop: Handle pointer enter with debounce
  const handlePointerEnter = () => {
    // Clear any pending leave timeout
    if (leaveTimeoutRef.current) {
      clearTimeout(leaveTimeoutRef.current);
      leaveTimeoutRef.current = null;
    }

    if (sidebarMode === 'hover') {
      // Debounce expand by 100ms to prevent flicker
      enterTimeoutRef.current = setTimeout(() => {
        setIsExpanded(true);
      }, 100);
    }
  };

  // Desktop: Handle pointer leave with debounce
  const handlePointerLeave = () => {
    // Clear any pending enter timeout
    if (enterTimeoutRef.current) {
      clearTimeout(enterTimeoutRef.current);
      enterTimeoutRef.current = null;
    }

    if (sidebarMode === 'hover') {
      // Debounce collapse by 500ms for natural feel
      leaveTimeoutRef.current = setTimeout(() => {
        setIsExpanded(false);
      }, 500);
    }
  };

  // Cleanup timeouts on unmount
  useEffect(() => {
    return () => {
      if (enterTimeoutRef.current) clearTimeout(enterTimeoutRef.current);
      if (leaveTimeoutRef.current) clearTimeout(leaveTimeoutRef.current);
    };
  }, []);

  const handleSidebarModeChange = (mode) => {
    setSidebarMode(mode);
    setMenuOpen(false);
    
    if (mode === 'expanded') {
      setIsExpanded(true);
    } else if (mode === 'collapsed') {
      setIsExpanded(false);
    } else {
      // 'hover' mode
      setIsExpanded(false);
    }
  };

  // Determine if sidebar should be shown as expanded
  const shouldShowExpanded = sidebarMode === 'expanded' || (sidebarMode === 'hover' && isExpanded);

  // Desktop Nav Item
  const NavItem = ({ to, icon: Icon, label }) => {
    const isActive = location.pathname === to || (to !== '/' && location.pathname.startsWith(to));
    const showText = shouldShowExpanded;
    
    return (
      <Link 
        to={to} 
        className={`flex items-center gap-3 py-3 rounded-lg transition-all duration-200 group relative ${
          showText ? 'px-4' : 'px-4 md:justify-center'
        } ${
          isActive 
            ? 'bg-brand-blue/15 text-brand-blue font-bold shadow-sm border-l-4 border-brand-blue' 
            : 'text-slate-500 hover:bg-slate-100 hover:text-slate-900 border-l-4 border-transparent'
        }`}
      >
        <Icon size={20} className={`shrink-0 ${isActive ? 'text-brand-blue' : 'text-slate-400 group-hover:text-brand-blue transition-colors'}`} strokeWidth={isActive ? 2.5 : 2} />
        <span className={`whitespace-nowrap transition-opacity duration-200 ${showText ? 'opacity-100 md:inline' : 'opacity-0 md:hidden md:w-0'} inline`}>
          {label}
        </span>
      </Link>
    );
  };

  // Mobile Bottom Tab Item
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

  const menuOptions = [
    { id: 'expanded', label: 'Expanded' },
    { id: 'collapsed', label: 'Collapsed' },
    { id: 'hover', label: 'Expand on hover' }
  ];

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden isolate relative">
      {/* Global Alert */}
      <div className="fixed top-0 left-0 right-0 z-[60]">
         <AlertBanner />
      </div>

      {/* Desktop Sidebar - Hidden on Mobile */}
      <aside 
        onPointerEnter={handlePointerEnter}
        onPointerLeave={handlePointerLeave}
        className={`
          hidden md:flex 
          fixed inset-y-0 left-0 z-50
          bg-white border-r border-slate-100 flex-col
          transition-all duration-300 ease-in-out
          shadow-xl md:shadow-lg
          ${shouldShowExpanded ? 'w-72' : 'w-20'}
        `}
      >
        {/* Main sidebar content */}
        <div className={`flex-1 flex flex-col ${shouldShowExpanded ? 'p-6' : 'p-3'} transition-all duration-300`}>
          {/* Brand */}
          <div className={`flex items-center gap-3 mb-10 ${shouldShowExpanded ? '' : 'justify-center'}`}>
             <img 
               src="/logo.png" 
               alt="Athenaeum Logo" 
               className="w-10 h-10 shrink-0 object-contain"
             />
             {shouldShowExpanded && (
               <div className="transition-opacity duration-200 animate-fade-in block">
                 <h1 className="text-lg font-bold tracking-tight text-brand-dark whitespace-nowrap">GPA's</h1>
                 <p className="text-xs text-slate-500 font-medium whitespace-nowrap">Library Management System</p>
               </div>
             )}
          </div>

          {/* Primary Navigation */}
          <div className="space-y-1">
            <p className={`text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 px-4 ${shouldShowExpanded ? 'opacity-100' : 'opacity-0 hidden'}`}>Menu</p>
            <NavItem to="/" icon={LayoutDashboard} label="Dashboard" />
            <NavItem to="/books" icon={BookOpen} label="Book Catalogue" />
            <NavItem to="/history" icon={Clock} label="History" />
            <NavItem to="/services" icon={FileText} label="Requests" />
          </div>

          {/* Spacer */}
          <div className="flex-1"></div>

          {/* Secondary Navigation (Account) */}
          <div className="space-y-1 border-t border-slate-100 pt-4">
            <p className={`text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 px-4 ${shouldShowExpanded ? 'opacity-100' : 'opacity-0 hidden'}`}>Account</p>
            <NavItem to="/profile" icon={User} label="Profile" />
            <NavItem to="/settings" icon={Settings} label="Settings" />
            
            <button 
              onClick={handleLogout} 
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-slate-500 hover:bg-red-50 hover:text-red-600 transition-all border-l-4 border-transparent ${
                shouldShowExpanded ? '' : 'justify-center'
              }`}
            >
              <LogOut size={20} className="shrink-0" />
              <span className={`transition-opacity duration-200 ${shouldShowExpanded ? 'opacity-100 inline' : 'opacity-0 hidden w-0'} whitespace-nowrap`}>
                Logout
              </span>
            </button>
          </div>
        </div>

        {/* Sidebar Control Menu - Positioned above footer */}
        {menuOpen && (
          <div 
            ref={menuRef}
            className="hidden md:block absolute bottom-20 left-2 w-44 bg-white border border-slate-200 rounded-md shadow-lg z-[60]"
            style={{ 
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.08)',
              fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
            }}
          >
            <div className="text-xs font-medium text-slate-500 px-3 py-2 block">
              Sidebar control
            </div>
            <div className="flex flex-col">
              {menuOptions.map((option) => (
                <button
                  key={option.id}
                  className={`flex items-center gap-2 px-3 py-2 text-sm font-normal transition-colors border-none cursor-pointer w-full text-left ${
                    sidebarMode === option.id 
                      ? 'bg-brand-blue/10 text-brand-dark' 
                      : 'bg-transparent text-slate-900 hover:bg-slate-100'
                  }`}
                  onClick={() => handleSidebarModeChange(option.id)}
                >
                  <span className={`w-2 h-2 rounded-full flex-shrink-0 ${
                    sidebarMode === option.id 
                      ? 'border-2 border-brand-blue bg-brand-blue' 
                      : 'border border-slate-300 bg-transparent'
                  }`} />
                  <span>{option.label}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Collapse/Expand button - Desktop only - Bottom footer */}
        <div className="hidden md:flex items-center justify-center h-14 border-t border-slate-100 bg-white">
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className={`p-2 rounded-lg transition-all duration-150 ${
              menuOpen ? 'text-brand-blue bg-brand-blue/10' :
              sidebarMode === 'expanded' ? 'text-brand-blue bg-brand-blue/10' :
              'text-slate-400 opacity-60'
            } hover:opacity-100 hover:bg-slate-100`}
          >
            {shouldShowExpanded ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
          </button>
        </div>
      </aside>

      {/* Main Content Area - Fixed left margin for collapsed sidebar (0 margin for Mobile) */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative ml-0 md:ml-20">
        
        {/* Header */}
        <header className="h-auto md:h-20 flex flex-col md:flex-row md:items-center justify-between px-4 py-4 md:py-0 md:px-10 bg-white/80 backdrop-blur-xl sticky top-0 z-30 border-b border-slate-100">
           
           {/* Top Row: Title & ID (Desktop) */}
           <div className="flex items-center justify-between w-full md:w-auto">
             <div>
                {/* Breadcrumbs - Integrated into header flow */}
                <div className="md:hidden mb-1">
                  <Breadcrumbs />
                </div>
                
                <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                  {location.pathname === '/' ? `Hello, ${user?.name || 'Student'}` : 
                   location.pathname === '/settings' ? 'Settings' :
                   location.pathname === '/profile' ? 'My Profile' :
                   location.pathname === '/services' ? 'Services & Notices' :
                   location.pathname === '/history' ? 'My Library Journey' :
                   location.pathname.startsWith('/books') ? 'Book Discovery' : 'Library'}
                </h2>
                
                <div className="hidden md:block mt-1">
                   <Breadcrumbs />
                </div>
             </div>

             {/* Mobile Profile Icon (for dropdown) */}
             <div className="md:hidden">
                <button 
                   onClick={() => setProfileMenuOpen(!profileMenuOpen)}
                   className="w-9 h-9 rounded-full bg-slate-100 border border-slate-200 overflow-hidden"
                >
                   <img 
                     src="https://images.unsplash.com/photo-1599566150163-29194dcaad36?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80" 
                     alt="Profile" 
                     className="w-full h-full object-cover" 
                   />
                </button>
             </div>
           </div>

           {/* Desktop Right Side Controls */}
           <div className="hidden md:flex items-center gap-3 md:gap-6">
              <div className="hidden md:flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-full text-sm text-slate-600 font-medium shadow-sm">
                 <ScanLine size={16} className="text-slate-400" />
                 {user?.enrollment_no || 'My ID'}
              </div>
              
           </div>

           {/* Shared Profile Dropdown (Positioned relative to Header) */}
           {profileMenuOpen && (
             <div className="absolute right-4 top-16 md:top-20 w-64 bg-white rounded-xl shadow-xl border border-slate-100 py-2 z-50 animate-fade-in origin-top-right">
               <div className="px-4 py-3 border-b border-slate-100">
                 <p className="text-sm font-bold text-brand-dark truncate">{user?.name || 'Student'}</p>
                 <p className="text-xs text-slate-500 truncate">{user?.email || 'student@university.edu'}</p>
               </div>
               <div className="py-2">
                 <Link to="/" onClick={() => setProfileMenuOpen(false)} className="flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 hover:text-brand-blue transition-colors"><Home size={16} />Dashboard</Link>
                 <Link to="/profile" onClick={() => setProfileMenuOpen(false)} className="flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 hover:text-brand-blue transition-colors"><User size={16} />Profile</Link>
                 <Link to="/settings" onClick={() => setProfileMenuOpen(false)} className="flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 hover:text-brand-blue transition-colors"><Settings size={16} />Settings</Link>
               </div>
               <div className="pt-1 border-t border-slate-100">
                 <button onClick={() => { setProfileMenuOpen(false); handleLogout(); }} className="w-full flex items-center gap-3 px-4 py-2.5 text-sm font-bold text-red-600 hover:bg-red-50 transition-colors text-left"><LogOut size={16} />Logout</button>
               </div>
             </div>
           )}
        </header>

        {/* Scrollable Page Content - Padding bottom for mobile tabs */}
        <main className="flex-1 overflow-y-auto p-4 md:p-10 pb-24 md:pb-10 scroll-smooth bg-slate-50">
          <Outlet />
        </main>

        {/* Mobile Bottom Tab Bar */}
        <div className="md:hidden fixed bottom-0 left-0 w-full bg-white border-t border-slate-200 px-2 py-1 safe-area-pb z-50 flex justify-between items-center shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
            <MobileTabItem to="/" icon={Home} label="Home" />
            <MobileTabItem to="/books" icon={BookOpen} label="Books" />
            <MobileTabItem to="/services" icon={FileText} label="Requests" />
            <MobileTabItem to="/history" icon={Clock} label="History" />
            <MobileTabItem to="/profile" icon={User} label="Profile" />
        </div>
      </div>
    </div>
  );
}

