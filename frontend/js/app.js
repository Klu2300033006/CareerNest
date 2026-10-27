/**
 * CareerNest — Global App Logic
 * Navbar scroll, mobile menu, theme toggle, profile dropdown
 */

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initThemeToggle();
    initProfileDropdown();
    initScrollReveal();
    updateAuthUI();
});

// ── Navbar scroll effect ──
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 30);
    });

    // Mobile menu
    const toggle = document.querySelector('.menu-toggle');
    const links = document.querySelector('.navbar-links');
    if (toggle && links) {
        toggle.addEventListener('click', () => {
            toggle.classList.toggle('active');
            links.classList.toggle('mobile-open');
        });
    }
}

// ── Theme Toggle (Dark / Light) ──
function initThemeToggle() {
    const saved = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);

    document.querySelectorAll('.theme-toggle').forEach(btn => {
        btn.innerHTML = saved === 'dark' ? '☀️' : '🌙';
        btn.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            btn.innerHTML = next === 'dark' ? '☀️' : '🌙';
        });
    });
}

// ── Profile Dropdown ──
function initProfileDropdown() {
    const trigger = document.querySelector('.profile-trigger');
    const menu = document.querySelector('.profile-dropdown');
    if (!trigger || !menu) return;

    trigger.addEventListener('click', (e) => {
        e.stopPropagation();
        menu.classList.toggle('active');
    });

    document.addEventListener('click', () => menu.classList.remove('active'));

    // Logout button
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            api.clearTokens();
            window.location.href = 'login.html';
        });
    }
}

// ── Update Auth UI ──
function updateAuthUI() {
    const user = api.getUser();
    const loggedIn = api.isLoggedIn();

    // Show/hide auth buttons
    document.querySelectorAll('.auth-only').forEach(el => {
        el.style.display = loggedIn ? '' : 'none';
    });
    document.querySelectorAll('.guest-only').forEach(el => {
        el.style.display = loggedIn ? 'none' : '';
    });

    // User name/avatar
    if (user) {
        document.querySelectorAll('.user-name').forEach(el => {
            el.textContent = user.full_name || 'User';
        });
        document.querySelectorAll('.user-email').forEach(el => {
            el.textContent = user.email || '';
        });
        document.querySelectorAll('.user-avatar-text').forEach(el => {
            el.textContent = getInitials(user.full_name);
        });
    }
}

// ── Mobile sidebar toggle ──
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) sidebar.classList.toggle('mobile-open');
}
