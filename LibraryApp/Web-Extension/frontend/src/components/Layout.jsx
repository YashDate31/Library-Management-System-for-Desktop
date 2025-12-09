import { Outlet, Link, useLocation } from 'react-router-dom';
import { LogOut, LayoutDashboard, BookOpen, Clock, FileText, Bell, Search, User, Settings, ScanLine, Menu, X, ChevronLeft, ChevronRight, Home, PanelLeftClose, PanelLeftOpen } from 'lucide-react';
import axios from 'axios';
import { useState, useEffect, useRef } from 'react';
import Breadcrumbs from './Breadcrumbs';
import AlertBanner from './AlertBanner';

export default function Layout({ user, setUser }) {
  const location = useLocation();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);
  const profileMenuRef = useRef(null);

  const handleLogout = async () => {
    await axios.post('/api/logout');
    setUser(null);
  };

  // Close profile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target)) {
        setProfileMenuOpen(false);
      }
    };
    if (profileMenuOpen) document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [profileMenuOpen]);

  // Desktop Nav Item
  const NavItem = ({ to, icon: Icon, label }) => {
    const isActive = location.pathname === to || (to !== '/' && location.pathname.startsWith(to));
    
    return (
      <Link 
        to={to} 
        title={isCollapsed ? label : ''}
        className={`flex items-center gap-3 py-3 rounded-lg transition-all duration-200 group relative ${
          isCollapsed ? 'justify-center px-2' : 'px-4'
        } ${
          isActive 
            ? 'bg-brand-blue/10 text-brand-blue font-bold' 
            : 'text-slate-500 hover:bg-slate-100 hover:text-slate-900'
        }`}
      >
        <Icon size={22} className={`shrink-0 transition-colors ${isActive ? 'text-brand-blue' : 'text-slate-400 group-hover:text-slate-600'}`} strokeWidth={isActive ? 2.5 : 2} />
        
        {!isCollapsed && (
          <span className="whitespace-nowrap transition-opacity duration-200 animate-fade-in block">
            {label}
          </span>
        )}
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

  const sidebarWidth = isCollapsed ? 'w-[70px]' : 'w-[260px]';
  const mainMargin = isCollapsed ? 'ml-0 md:ml-[70px]' : 'ml-0 md:ml-[260px]';

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden isolate relative">
      {/* Global Alert */}
      <div className="fixed top-0 left-0 right-0 z-[60]">
         <AlertBanner />
      </div>

      {/* Desktop Sidebar */}
      <aside 
        className={`
          hidden md:flex 
          fixed inset-y-0 left-0 z-50
          bg-white border-r border-slate-200 flex-col
          transition-all duration-300 ease-in-out
          ${sidebarWidth}
        `}
      >
        {/* Sidebar Header */}
        <div className={`h-20 flex items-center ${isCollapsed ? 'justify-center' : 'px-6 justify-between'} border-b border-slate-50`}>
           <div className="flex items-center gap-3 overflow-hidden">
             <img src="/logo.png" alt="Logo" className="w-8 h-8 object-contain shrink-0" />
             {!isCollapsed && (
               <div className="whitespace-nowrap transition-opacity duration-300">
                 <h1 className="text-lg font-bold text-slate-800 tracking-tight">GPA's Library</h1>
               </div>
             )}
           </div>
           
           {!isCollapsed && (
             <button onClick={() => setIsCollapsed(true)} className="text-slate-400 hover:text-slate-600 transition-colors">
               <PanelLeftClose size={18} />
             </button>
           )}
        </div>

        {/* Navigation */}
        <div className="flex-1 flex flex-col py-6 px-3 gap-1 overflow-y-auto scrollbar-hide">
           {/* Section Label */}
           {!isCollapsed && <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 px-3">Menu</p>}
           
           <NavItem to="/" icon={LayoutDashboard} label="Dashboard" />
           <NavItem to="/books" icon={BookOpen} label="Catalogue" />
           <NavItem to="/history" icon={Clock} label="History" />
           <NavItem to="/services" icon={FileText} label="Services" />

           {!isCollapsed && <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mt-6 mb-2 px-3">Account</p>}
           {isCollapsed && <div className="h-4"></div>} {/* Spacer for collapsed */}
           
           <NavItem to="/profile" icon={User} label="Profile" />
           <NavItem to="/settings" icon={Settings} label="Settings" />
        </div>

        {/* Sidebar Footer (User / Logout) */}
        <div className="p-3 border-t border-slate-100">
           {isCollapsed ? (
             <button onClick={() => setIsCollapsed(false)} className="w-full flex justify-center py-3 text-slate-400 hover:text-brand-blue hover:bg-slate-50 rounded-lg transition-colors">
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
      <div className={`flex-1 flex flex-col min-w-0 overflow-hidden relative transition-all duration-300 ease-in-out ${mainMargin}`}>
        
        {/* Mobile Header (unchanged logic) */}
        <header className="h-auto md:h-20 flex flex-col md:flex-row md:items-center justify-between px-4 py-4 md:py-0 md:px-10 bg-white/80 backdrop-blur-xl sticky top-0 z-30 border-b border-slate-100">
           <div className="flex items-center justify-between w-full md:w-auto">
             <div>
                <div className="md:hidden mb-1"><Breadcrumbs /></div>
                <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                  {location.pathname === '/' ? `Hello, ${user?.name || 'Student'}` : 
                   location.pathname.includes('books') ? 'Library Catalogue' :
                   location.pathname.replace('/', '').charAt(0).toUpperCase() + location.pathname.slice(2)}
                </h2>
                <div className="hidden md:block mt-1"><Breadcrumbs /></div>
             </div>

             {/* Mobile User Avatar */}
             <div className="md:hidden relative" ref={profileMenuRef}>
                <button 
                   onClick={() => setProfileMenuOpen(!profileMenuOpen)}
                   className="w-9 h-9 rounded-full bg-slate-100 border border-slate-200 overflow-hidden"
                >
                   <div className="w-full h-full flex items-center justify-center text-slate-500 font-bold">
                     {user?.name?.charAt(0)}
                   </div>
                </button>
                {/* Mobile Dropdown */}
                {profileMenuOpen && (
                  <div className="absolute right-0 top-12 w-48 bg-white rounded-xl shadow-xl border border-slate-100 py-1 z-50 animate-fade-in">
                    <Link to="/settings" className="flex items-center gap-2 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50"><Settings size={14}/> Settings</Link>
                    <button onClick={handleLogout} className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 text-left"><LogOut size={14}/> Logout</button>
                  </div>
                )}
             </div>
           </div>

           {/* Desktop Right Controls (ID Badge) */}
           <div className="hidden md:flex items-center gap-4">
              <div className="flex items-center gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm font-mono text-slate-600 shadow-sm">
                 <ScanLine size={14} className="text-slate-400" />
                 {user?.enrollment_no || '0000'}
              </div>
           </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-4 md:p-10 pb-24 md:pb-10 scroll-smooth bg-slate-50">
          <Outlet />
        </main>

        {/* Mobile Tab Bar */}
        <div className="md:hidden fixed bottom-6 left-4 right-4 h-16 bg-white rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.12)] border border-slate-100 z-50 flex justify-between items-center px-6">
             <MobileTabItem to="/" icon={Home} label="Home" />
             <MobileTabItem to="/books" icon={BookOpen} label="Books" />
             <MobileTabItem to="/services" icon={FileText} label="Services" />
             <MobileTabItem to="/profile" icon={User} label="Profile" />
        </div>
      </div>
    </div>
  );
}

