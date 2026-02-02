import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import axios from 'axios'
import { getCsrfToken } from './utils/csrf'
import { registerSW } from 'virtual:pwa-register'

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

// --- PWA: auto-update + auto-reload on new version ---
// Prevent clients from being stuck on an old UI due to service worker caching.
const updateSW = registerSW({
  immediate: true,
  onNeedRefresh() {
    // Activate the new service worker and reload to fetch fresh assets.
    Promise.resolve(updateSW(true)).finally(() => {
      window.location.reload();
    });
  },
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

