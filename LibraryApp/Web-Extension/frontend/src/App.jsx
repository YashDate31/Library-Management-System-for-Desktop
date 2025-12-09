import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Catalogue from './pages/Catalogue';
import BookDetails from './pages/BookDetails';
import Settings from './pages/Settings';
import History from './pages/History';
import Services from './pages/Services';
import Layout from './components/Layout';
import { useState, useEffect } from 'react';
import axios from 'axios';

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
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={!user ? <Login setUser={setUser} /> : <Navigate to="/" />} />
        
        <Route element={<Layout user={user} setUser={setUser} />}>
          <Route path="/" element={user ? <Dashboard user={user} /> : <Navigate to="/login" />} />
          <Route path="/books" element={user ? <Catalogue /> : <Navigate to="/login" />} />
          <Route path="/books/:bookId" element={user ? <BookDetails /> : <Navigate to="/login" />} />
          <Route path="/history" element={user ? <History /> : <Navigate to="/login" />} />
          <Route path="/services" element={user ? <Services /> : <Navigate to="/login" />} />
          <Route path="/settings" element={user ? <Settings user={user} setUser={setUser} /> : <Navigate to="/login" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
