import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import axios from 'axios'
import { getCsrfToken } from './utils/csrf'

// --- CSRF Protection: Add token to all state-changing requests ---
axios.interceptors.request.use((config) => {
  // Add CSRF token for POST, PUT, DELETE, PATCH methods
  if (['post', 'put', 'delete', 'patch'].includes(config.method?.toLowerCase())) {
    const token = getCsrfToken();
    if (token) {
      config.headers['X-CSRF-Token'] = token;
    }
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

