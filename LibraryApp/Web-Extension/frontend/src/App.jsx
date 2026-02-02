import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Catalogue from './pages/Catalogue';
import BookDetails from './pages/BookDetails';
import Settings from './pages/Settings';
import Notifications from './pages/Notifications';
import Profile from './pages/Profile';
import History from './pages/History';
import MyBooks from './pages/MyBooks';
import Services from './pages/Services';
import StudyMaterials from './pages/StudyMaterials';
import Contact from './pages/Contact';
import Layout from './components/Layout';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { ToastProvider } from './context/ToastContext';
import ErrorBoundary from './components/ErrorBoundary';

function AppRoutes({ user, setUser }) {
  const location = useLocation();
  
  return (
    <Routes location={location} key={location.pathname}>
      <Route path="/login" element={!user ? <Login setUser={setUser} /> : <Navigate to="/" replace />} />
      <Route path="/register" element={!user ? <Register /> : <Navigate to="/" replace />} />
      
      <Route element={<Layout user={user} setUser={setUser} />}>
        <Route path="/" element={user ? <Dashboard user={user} /> : <Navigate to="/login" replace />} />
        <Route path="/books" element={user ? <Catalogue /> : <Navigate to="/login" replace />} />
        <Route path="/books/:bookId" element={user ? <BookDetails /> : <Navigate to="/login" replace />} />
        <Route path="/my-books" element={user ? <MyBooks user={user} /> : <Navigate to="/login" replace />} />
        <Route path="/history" element={user ? <History user={user} /> : <Navigate to="/login" replace />} />
        <Route path="/services" element={user ? <Services /> : <Navigate to="/login" replace />} />
        <Route path="/study-materials" element={user ? <StudyMaterials user={user} /> : <Navigate to="/login" replace />} />
        <Route path="/requests" element={user ? <Services /> : <Navigate to="/login" replace />} />
        <Route path="/profile" element={user ? <Profile user={user} /> : <Navigate to="/login" replace />} />
        <Route path="/settings" element={user ? <Settings user={user} setUser={setUser} /> : <Navigate to="/login" replace />} />
        <Route path="/contact" element={user ? <Contact /> : <Navigate to="/login" replace />} />
        <Route path="/notifications" element={user ? <Notifications /> : <Navigate to="/login" replace />} />
      </Route>
    </Routes>
  );
}

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check session on mount and Initialize Theme
  useEffect(() => {
    checkSession();
    
    // Initialize Theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  const checkSession = async () => {
    try {
      const { data } = await axios.get('/api/me');
      if (data.user) setUser(data.user);
    } catch (e) {
      console.log('Not logged in');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="h-screen flex items-center justify-center bg-background text-text-primary">Loading...</div>;

  return (
    <ToastProvider>
      <BrowserRouter>
        <ErrorBoundary>
          <AppRoutes user={user} setUser={setUser} />
        </ErrorBoundary>
      </BrowserRouter>
    </ToastProvider>
  );
}

export default App;
