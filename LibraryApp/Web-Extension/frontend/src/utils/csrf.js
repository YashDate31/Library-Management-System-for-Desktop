/**
 * CSRF Token Utility
 * Reads the CSRF token from the cookie set by the server
 */

export function getCsrfToken() {
  const match = document.cookie.match(/csrf_token=([^;]+)/);
  return match ? match[1] : null;
}

export default getCsrfToken;
