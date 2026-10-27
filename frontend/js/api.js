/**
 * CareerNest — API Client
 * Centralized fetch wrapper with JWT authentication
 */

// Auto-detect: use deployed backend on Render, or localhost for dev
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/api'
    : 'https://careernest-backend-y6nh.onrender.com/api';

const api = {
    getToken() {
        return localStorage.getItem('access_token');
    },

    getRefreshToken() {
        return localStorage.getItem('refresh_token');
    },

    setTokens(access, refresh) {
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    },

    clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
    },

    getUser() {
        const u = localStorage.getItem('user');
        return u ? JSON.parse(u) : null;
    },

    setUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    },

    isLoggedIn() {
        return !!this.getToken();
    },

    isAdmin() {
        const user = this.getUser();
        return user && user.is_staff;
    },

    async request(endpoint, method = 'GET', body = null, isFormData = false) {
        const url = `${API_BASE}${endpoint}`;
        const headers = {};

        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        if (!isFormData) {
            headers['Content-Type'] = 'application/json';
        }

        const config = { method, headers };

        if (body) {
            config.body = isFormData ? body : JSON.stringify(body);
        }

        try {
            let response = await fetch(url, config);

            // Token expired — try refresh
            if (response.status === 401 && this.getRefreshToken()) {
                const refreshed = await this.refreshToken();
                if (refreshed) {
                    headers['Authorization'] = `Bearer ${this.getToken()}`;
                    config.headers = headers;
                    response = await fetch(url, config);
                } else {
                    this.clearTokens();
                    window.location.href = 'login.html';
                    return null;
                }
            }

            const data = await response.json().catch(() => null);

            if (!response.ok) {
                throw { status: response.status, data };
            }

            return data;
        } catch (error) {
            if (error.status) throw error;
            console.error('Network error:', error);
            throw { status: 0, data: { error: 'Network error. Please check your connection.' } };
        }
    },

    async refreshToken() {
        try {
            const res = await fetch(`${API_BASE}/auth/token/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: this.getRefreshToken() }),
            });
            if (res.ok) {
                const data = await res.json();
                this.setTokens(data.access, data.refresh || this.getRefreshToken());
                return true;
            }
            return false;
        } catch {
            return false;
        }
    },

    // Shorthand methods
    get(endpoint) { return this.request(endpoint); },
    post(endpoint, body) { return this.request(endpoint, 'POST', body); },
    put(endpoint, body) { return this.request(endpoint, 'PUT', body); },
    patch(endpoint, body) { return this.request(endpoint, 'PATCH', body); },
    delete(endpoint) { return this.request(endpoint, 'DELETE'); },
    upload(endpoint, formData) { return this.request(endpoint, 'POST', formData, true); },
};
