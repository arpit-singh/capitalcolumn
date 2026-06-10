/**
 * API client with JWT authentication.
 * All requests go through this module so auth is handled consistently.
 */

const API_URL = import.meta.env.VITE_API_URL || '';

function getToken() {
  return localStorage.getItem('cc_admin_token');
}

function authHeaders() {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return headers;
}

async function handleResponse(res) {
  if (res.status === 401) {
    localStorage.removeItem('cc_admin_token');
    localStorage.removeItem('cc_admin_user');
    window.location.href = '/';
    throw new Error('Unauthorized');
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

export async function get(path, params = {}) {
  const base = API_URL || window.location.origin;
  const url = new URL(`${API_URL}${path}`, base);
  Object.entries(params).forEach(([k, v]) => {
    if (v !== null && v !== undefined && v !== '') url.searchParams.set(k, v);
  });
  const res = await fetch(url.toString(), { headers: authHeaders() });
  return handleResponse(res);
}

export async function post(path, body = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(body),
  });
  return handleResponse(res);
}

export async function patch(path, body = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    method: 'PATCH',
    headers: authHeaders(),
    body: JSON.stringify(body),
  });
  return handleResponse(res);
}

export async function uploadFile(path, formData) {
  const token = getToken();
  const headers = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;
  // Don't set Content-Type — browser sets it with boundary for FormData
  const res = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers,
    body: formData,
  });
  return handleResponse(res);
}

export async function login(email, password) {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || 'Login failed');
  }
  const data = await res.json();
  localStorage.setItem('cc_admin_token', data.access_token);

  // Fetch user profile
  const userRes = await fetch(`${API_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${data.access_token}` },
  });
  if (userRes.ok) {
    const user = await userRes.json();
    localStorage.setItem('cc_admin_user', JSON.stringify(user));
    return user;
  }
  return null;
}

export function logout() {
  localStorage.removeItem('cc_admin_token');
  localStorage.removeItem('cc_admin_user');
  window.location.href = '/';
}

export function getUser() {
  const u = localStorage.getItem('cc_admin_user');
  return u ? JSON.parse(u) : null;
}

export function isAuthenticated() {
  return !!getToken();
}
