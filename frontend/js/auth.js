/**
 * CareerNest — Auth (Login & Register)
 */

document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');

    if (registerForm) initRegister(registerForm);
    if (loginForm) initLogin(loginForm);
});

function initRegister(form) {
    const passwordInput = document.getElementById('reg-password');
    if (passwordInput) {
        passwordInput.addEventListener('input', () => updatePasswordStrength(passwordInput.value));
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const alert = document.querySelector('.auth-alert');
        const btn = form.querySelector('.auth-submit');

        const fullName = document.getElementById('reg-name').value.trim();
        const email = document.getElementById('reg-email').value.trim();
        const password = document.getElementById('reg-password').value;
        const confirmPassword = document.getElementById('reg-confirm').value;

        // Validation
        if (!fullName || !email || !password || !confirmPassword) {
            showAuthAlert(alert, 'Please fill in all fields.', 'error');
            return;
        }
        if (password.length < 8) {
            showAuthAlert(alert, 'Password must be at least 8 characters.', 'error');
            return;
        }
        if (password !== confirmPassword) {
            showAuthAlert(alert, 'Passwords do not match.', 'error');
            return;
        }

        btn.classList.add('btn-loading');
        btn.innerHTML = '<span class="btn-text">Creating Account...</span>';

        try {
            const data = await api.post('/auth/register/', {
                full_name: fullName, email, password, confirm_password: confirmPassword,
            });
            api.setTokens(data.tokens.access, data.tokens.refresh);
            api.setUser(data.user);
            showAuthAlert(alert, 'Account created! Redirecting...', 'success');
            setTimeout(() => window.location.href = 'dashboard.html', 1000);
        } catch (err) {
            const msg = err.data ? Object.values(err.data).flat().join(' ') : 'Registration failed.';
            showAuthAlert(alert, msg, 'error');
            btn.classList.remove('btn-loading');
            btn.innerHTML = 'Create Account';
        }
    });
}

function initLogin(form) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const alert = document.querySelector('.auth-alert');
        const btn = form.querySelector('.auth-submit');

        const email = document.getElementById('login-email').value.trim();
        const password = document.getElementById('login-password').value;

        if (!email || !password) {
            showAuthAlert(alert, 'Please enter your email and password.', 'error');
            return;
        }

        btn.classList.add('btn-loading');
        btn.innerHTML = '<span class="btn-text">Signing In...</span>';

        try {
            const data = await api.post('/auth/login/', { email, password });
            api.setTokens(data.tokens.access, data.tokens.refresh);
            api.setUser(data.user);
            showAuthAlert(alert, 'Login successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = data.user.is_staff ? 'admin-panel.html' : 'dashboard.html';
            }, 800);
        } catch (err) {
            const msg = err.data?.error || 'Invalid email or password.';
            showAuthAlert(alert, msg, 'error');
            btn.classList.remove('btn-loading');
            btn.innerHTML = 'Sign In';
        }
    });
}

function showAuthAlert(el, message, type) {
    if (!el) return;
    el.className = `auth-alert show alert-${type}`;
    el.innerHTML = `<span>${type === 'error' ? '✕' : '✓'}</span> ${message}`;
}

function updatePasswordStrength(password) {
    const bars = document.querySelectorAll('.strength-bar');
    const text = document.querySelector('.strength-text');
    if (!bars.length) return;

    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password) && /[a-z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    const levels = ['', 'Weak', 'Fair', 'Good', 'Strong'];
    const classes = ['', 'weak', 'weak', 'medium', 'strong'];

    bars.forEach((bar, i) => {
        bar.className = 'strength-bar';
        if (i < strength) bar.classList.add(classes[strength]);
    });
    if (text) text.textContent = password ? levels[strength] : '';
}
