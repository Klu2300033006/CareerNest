/**
 * CareerNest — Dashboard Page Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    if (!requireAuth()) return;
    loadDashboard();
});

async function loadDashboard() {
    const user = api.getUser();

    // Welcome message
    const welcomeEl = document.querySelector('.welcome-title');
    if (welcomeEl && user) {
        const hour = new Date().getHours();
        const greeting = hour < 12 ? 'Good Morning' : hour < 17 ? 'Good Afternoon' : 'Good Evening';
        welcomeEl.textContent = `${greeting}, ${user.full_name?.split(' ')[0] || 'there'}! 👋`;
    }

    const dateEl = document.querySelector('.welcome-subtitle');
    if (dateEl) {
        dateEl.textContent = new Date().toLocaleDateString('en-US', {
            weekday: 'long', month: 'long', day: 'numeric', year: 'numeric'
        });
    }

    // Load stats
    try {
        const stats = await api.get('/stats/');
        const counters = {
            'stat-total': stats.total_applications,
            'stat-pending': stats.pending,
            'stat-accepted': stats.accepted,
            'stat-rejected': stats.rejected,
        };
        Object.entries(counters).forEach(([id, value]) => {
            const el = document.getElementById(id);
            if (el) animateCounter(el, value);
        });
    } catch (e) {
        console.error('Failed to load stats:', e);
    }

    // Load recent applications
    try {
        const apps = await api.get('/applications/history/?page_size=5');
        const list = document.getElementById('recent-activity');
        if (list && apps.results) {
            if (apps.results.length === 0) {
                list.innerHTML = `<div class="empty-state" style="padding: 40px 20px;">
                    <div class="empty-state-icon">📋</div>
                    <div class="empty-state-title">No applications yet</div>
                    <div class="empty-state-text">Start applying to jobs to see your activity here.</div>
                    <a href="jobs.html" class="btn btn-primary btn-sm" style="margin-top: 12px;">Browse Jobs</a>
                </div>`;
            } else {
                list.innerHTML = apps.results.map(app => `
                    <div class="activity-item">
                        <div class="activity-icon">${app.job?.company?.name?.[0] || '?'}</div>
                        <div class="activity-info">
                            <div class="activity-title">${app.job?.title || 'Unknown Job'}</div>
                            <div class="activity-sub">${app.job?.company?.name || ''} · ${timeAgo(app.applied_at)}</div>
                        </div>
                        ${statusBadge(app.status)}
                    </div>
                `).join('');
            }
        }
    } catch (e) {
        console.error('Failed to load recent activity:', e);
    }
}
