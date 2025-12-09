import { useLocation, Link } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';

export default function Breadcrumbs() {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);

  const breadcrumbNameMap = {
    books: 'Book Catalogue',
    history: 'History',
    services: 'Services',
    profile: 'Profile',
    settings: 'Settings',
  };

  return (
    <nav className="flex items-center text-sm text-slate-500 my-1 fade-in">
      <Link to="/" className="hover:text-brand-blue flex items-center transition-colors">
        <Home size={14} className="mr-1" />
        Home
      </Link>
      
      {pathnames.map((value, index) => {
        const to = `/${pathnames.slice(0, index + 1).join('/')}`;
        const isLast = index === pathnames.length - 1;
        
        // Handle dynamic routes like /books/123 if needed, or just show ID
        let displayName = breadcrumbNameMap[value] || value;
        // Simple capitalization for unknown routes or IDs
        if (!breadcrumbNameMap[value]) {
            displayName = value.charAt(0).toUpperCase() + value.slice(1);
        }

        return (
          <span key={to} className="flex items-center">
            <ChevronRight size={14} className="mx-2 text-slate-300" />
            {isLast ? (
              <span className="font-semibold text-brand-blue">{displayName}</span>
            ) : (
              <Link to={to} className="hover:text-brand-blue transition-colors">
                {displayName}
              </Link>
            )}
          </span>
        );
      })}
    </nav>
  );
}
