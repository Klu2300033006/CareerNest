/**
 * CareerNest — Application History Page Logic
 */

let appCurrentView = 'cards';
let appStatusFilter = 'all';

document.addEventListener('DOMContentLoaded', () => {
    if (!requireAuth()) return;
    loadApplications();
    initAppControls();
});

function initAppControls() {
    // Status filter buttons
    document.querySelectorAll('.status-filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.status-filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            appStatusFilter = btn.dataset.status;
            loadApplications();
        });
    });

    // View toggle
    document.querySelectorAll('.view-toggle-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.view-toggle-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            appCurrentView = btn.dataset.view;
            loadApplications();
        });
    });
}

async function loadApplications() {
    const container = document.getElementById('applications-container');
    if (!container) return;

    try {
        const data = await api.get('/applications/history/');
        let apps = data.results || [];

        if (appStatusFilter !== 'all') {
            apps = apps.filter(a => a.status === appStatusFilter);
        }

        if (apps.length === 0) {
            container.innerHTML = `<div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <div class="empty-state-title">No applications found</div>
                <div class="empty-state-text">${appStatusFilter !== 'all' ? 'No ' + appStatusFilter + ' applications.' : 'You haven\'t applied to any jobs yet.'}</div>
                <a href="jobs.html" class="btn btn-primary btn-sm mt-4">Browse Jobs</a>
            </div>`;
            return;
        }

        if (appCurrentView === 'timeline') {
            renderTimeline(container, apps);
        } else {
            renderCards(container, apps);
        }
    } catch (e) {
        container.innerHTML = '<p class="text-center text-muted p-8">Failed to load applications.</p>';
    }
}

function renderCards(container, apps) {
    container.innerHTML = `<div class="applications-grid">${apps.map(app => {
        const job = app.job || {};
        const company = job.company || {};
        return `
        <div class="application-card">
            <div class="application-card-header">
                <div class="app-job-info">
                    <div class="app-job-logo">${company.name?.[0] || '?'}</div>
                    <div>
                        <div class="app-job-title">${job.title || 'Unknown'}</div>
                        <div class="app-job-company">${company.name || ''}</div>
                    </div>
                </div>
                ${statusBadge(app.status)}
            </div>
            <div class="application-card-body">
                <div class="app-detail">Applied<strong>${formatDate(app.applied_at)}</strong></div>
                <div class="app-detail">Location<strong>${job.location || 'N/A'}</strong></div>
                <div class="app-detail">Type<strong>${typeBadge(job.job_type || '')}</strong></div>
            </div>
            <div class="application-card-footer">
                <span class="text-xs text-muted">Last updated: ${formatDate(app.updated_at)}</span>
                <a href="job-detail.html?id=${job.id}" class="btn btn-ghost btn-sm">View Job</a>
            </div>
        </div>`;
    }).join('')}</div>`;
}

function renderTimeline(container, apps) {
    container.innerHTML = `<div class="timeline">${apps.map((app, i) => {
        const job = app.job || {};
        const company = job.company || {};
        return `
        <div class="timeline-item" style="animation-delay: ${i * 0.1}s">
            <div class="timeline-dot ${app.status}"></div>
            <div class="timeline-content">
                <div class="timeline-header">
                    <div class="timeline-title">${job.title || 'Unknown'}</div>
                    ${statusBadge(app.status)}
                </div>
                <div class="timeline-body">
                    <p>${company.name || ''} · ${job.location || ''}</p>
                    <p class="mt-2 text-xs text-muted">Applied ${formatDate(app.applied_at)}</p>
                </div>
            </div>
        </div>`;
    }).join('')}</div>`;
}
