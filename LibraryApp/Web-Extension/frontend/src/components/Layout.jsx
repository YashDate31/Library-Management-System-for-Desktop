import { Outlet, Link, useLocation } from 'react-router-dom';
import { LogOut, Library } from 'lucide-react';
import axios from 'axios';

export default function Layout({ user, setUser }) {
  const location = useLocation();

  const handleLogout = async () => {
    await axios.post('/api/logout');
    setUser(null);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="glass sticky top-0 z-50 px-8 py-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
           <div className="p-2 bg-gradient-to-br from-primary to-accent rounded-lg text-white">
             <Library size={24} />
           </div>
           <span className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
             LibraryConnect
           </span>
        </div>

        <div className="flex items-center gap-6">
          <Link to="/" className={`font-medium transition ${location.pathname === '/' ? 'text-primary' : 'text-slate-500 hover:text-slate-900'}`}>
            Dashboard
          </Link>
          <Link to="/books" className={`font-medium transition ${location.pathname === '/books' ? 'text-primary' : 'text-slate-500 hover:text-slate-900'}`}>
            Catalogue
          </Link>
          <button onClick={handleLogout} className="flex items-center gap-2 text-red-500 hover:text-red-700 font-medium transition">
            <LogOut size={18} />
            Sign Out
          </button>
        </div>
      </nav>

      <main className="flex-1 container mx-auto p-6 max-w-6xl animate-fade-in">
        <Outlet />
      </main>
    </div>
  );
}
