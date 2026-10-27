/**
 * CareerNest — Admin Panel Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    if (!requireAuth() || !requireAdmin()) return;
    loadAdminDashboard();
    initAdminControls();
});

async function loadAdminDashboard() {
    try {
        const stats = await api.get('/admin/stats/');
        const counters = {
            'admin-jobs': stats.total_jobs,
            'admin-users': stats.total_users,
            'admin-apps': stats.total_applications,
            'admin-rate': stats.acceptance_rate,
        };
        Object.entries(counters).forEach(([id, value]) => {
            const el = document.getElementById(id);
            if (el) animateCounter(el, Math.round(value));
        });
    } catch (e) { console.error('Admin stats error:', e); }

    loadAdminJobs();
    loadAdminApplications();
}

async function loadAdminJobs() {
    const tbody = document.getElementById('admin-jobs-table');
    if (!tbody) return;

    try {
        const data = await api.get('/jobs/');
        const jobs = data.results || [];
        tbody.innerHTML = jobs.map(job => `
            <tr>
                <td><strong>${job.title}</strong></td>
                <td>${job.company?.name || 'N/A'}</td>
                <td>${job.location}</td>
                <td><span class="badge badge-primary">${typeBadge(job.job_type)}</span></td>
                <td>${job.application_count || 0}</td>
                <td>${formatDate(job.created_at)}</td>
                <td class="actions">
                    <button class="action-btn" onclick="editJob(${job.id})" title="Edit">✏️</button>
                    <button class="action-btn delete" onclick="deleteJob(${job.id})" title="Delete">🗑️</button>
                </td>
            </tr>
        `).join('');
    } catch (e) { tbody.innerHTML = '<tr><td colspan="7" class="text-center p-4">Failed to load jobs</td></tr>'; }
}

async function loadAdminApplications() {
    const tbody = document.getElementById('admin-apps-table');
    if (!tbody) return;

    try {
        const data = await api.get('/admin/applications/');
        const apps = data.results || [];
        tbody.innerHTML = apps.map(app => `
            <tr>
                <td>${app.user_name || 'N/A'}</td>
                <td>${app.job?.title || 'N/A'}</td>
                <td>${app.user_email || ''}</td>
                <td>${formatDate(app.applied_at)}</td>
                <td>
                    <select class="status-select" onchange="updateAppStatus(${app.id}, this.value)">
                        <option value="pending" ${app.status==='pending'?'selected':''}>Pending</option>
                        <option value="reviewed" ${app.status==='reviewed'?'selected':''}>Reviewed</option>
                        <option value="accepted" ${app.status==='accepted'?'selected':''}>Accepted</option>
                        <option value="rejected" ${app.status==='rejected'?'selected':''}>Rejected</option>
                    </select>
                </td>
                <td><a href="${app.resume}" target="_blank" class="btn btn-ghost btn-sm">📄 View</a></td>
            </tr>
        `).join('');
    } catch (e) { tbody.innerHTML = '<tr><td colspan="6" class="text-center p-4">Failed to load</td></tr>'; }
}

async function updateAppStatus(appId, status) {
    try {
        await api.patch(`/applications/${appId}/status/`, { status });
        showToast(`Status updated to ${status}`, 'success');
    } catch (e) {
        showToast('Failed to update status', 'error');
    }
}

async function deleteJob(jobId) {
    if (!confirm('Are you sure you want to delete this job?')) return;
    try {
        await api.delete(`/jobs/${jobId}/delete/`);
        showToast('Job deleted successfully', 'success');
        loadAdminJobs();
    } catch (e) {
        showToast('Failed to delete job', 'error');
    }
}

function editJob(jobId) {
    showToast('Edit functionality — open modal with job data', 'info');
}

function initAdminControls() {
    // Add Job modal
    const addBtn = document.getElementById('add-job-btn');
    const modal = document.getElementById('add-job-modal');
    const closeBtn = modal?.querySelector('.modal-close');

    if (addBtn && modal) {
        addBtn.addEventListener('click', () => modal.classList.add('active'));
        closeBtn?.addEventListener('click', () => modal.classList.remove('active'));
        modal.addEventListener('click', (e) => { if (e.target === modal) modal.classList.remove('active'); });
    }

    // Add job form
    const addForm = document.getElementById('add-job-form');
    if (addForm) {
        addForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(addForm);
            const body = Object.fromEntries(formData.entries());
            try {
                await api.post('/jobs/create/', body);
                showToast('Job created successfully!', 'success');
                modal.classList.remove('active');
                addForm.reset();
                loadAdminJobs();
                loadAdminDashboard();
            } catch (err) {
                const msg = err.data ? Object.values(err.data).flat().join(' ') : 'Failed to create job.';
                showToast(msg, 'error');
            }
        });
    }
}
