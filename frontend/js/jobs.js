/**
 * CareerNest — Job Listings Page Logic
 */

let currentPage = 1;
let totalPages = 1;
let currentFilters = {};

document.addEventListener('DOMContentLoaded', () => {
    loadJobs();
    initJobSearch();
    initFilters();
});

async function loadJobs(page = 1) {
    const grid = document.getElementById('jobs-grid');
    if (!grid) return;

    showSkeletons(grid, 6);

    const params = new URLSearchParams();
    params.set('page', page);
    if (currentFilters.search) params.set('search', currentFilters.search);
    if (currentFilters.job_type) params.set('job_type', currentFilters.job_type);
    if (currentFilters.location) params.set('location', currentFilters.location);
    if (currentFilters.category) params.set('category', currentFilters.category);
    if (currentFilters.salary_min) params.set('salary_min', currentFilters.salary_min);
    if (currentFilters.salary_max) params.set('salary_max', currentFilters.salary_max);

    try {
        const data = await api.request(`/jobs/?${params.toString()}`, 'GET');
        const jobs = data.results || [];
        totalPages = Math.ceil((data.count || 0) / 12);
        currentPage = page;

        if (jobs.length === 0) {
            grid.innerHTML = `<div class="empty-state" style="grid-column: 1/-1;">
                <div class="empty-state-icon">🔍</div>
                <div class="empty-state-title">No jobs found</div>
                <div class="empty-state-text">Try adjusting your search or filters.</div>
            </div>`;
        } else {
            grid.innerHTML = jobs.map(job => renderJobCard(job)).join('');
        }

        renderPagination();
        updateResultCount(data.count || 0);
    } catch (e) {
        grid.innerHTML = '<p class="text-center text-muted" style="grid-column:1/-1;">Failed to load jobs.</p>';
        console.error(e);
    }
}

function renderJobCard(job) {
    const company = job.company || {};
    const logo = company.name ? company.name[0] : '?';
    const salary = formatSalary(job.salary_min, job.salary_max);
    const skills = job.skills ? job.skills.split(',').slice(0, 3) : [];
    const featured = job.is_featured ? ' featured' : '';

    return `
    <div class="job-card card-hover${featured}" onclick="window.location.href='job-detail.html?id=${job.id}'">
        <div class="job-card-header">
            <div class="job-company-logo">${logo}</div>
            <div class="job-card-info">
                <div class="job-card-title">${job.title}</div>
                <div class="job-card-company">${company.name || 'Unknown'}</div>
            </div>
        </div>
        <div class="job-card-meta">
            <span class="job-meta-item"><span class="meta-icon">📍</span> ${job.location}</span>
            <span class="job-meta-item"><span class="meta-icon">💼</span> ${typeBadge(job.job_type)}</span>
            ${job.experience_level ? `<span class="job-meta-item"><span class="meta-icon">📊</span> ${job.experience_level}</span>` : ''}
        </div>
        ${skills.length ? `<div class="job-card-tags">${skills.map(s => `<span class="job-tag">${s.trim()}</span>`).join('')}</div>` : ''}
        <div class="job-card-footer">
            <span class="job-salary">${salary}</span>
            <span class="job-posted">${formatDate(job.created_at)}</span>
        </div>
    </div>`;
}

function initJobSearch() {
    const input = document.getElementById('job-search');
    if (!input) return;
    input.addEventListener('input', debounce(() => {
        currentFilters.search = input.value;
        loadJobs(1);
    }, 400));
}

function initFilters() {
    // Job type checkboxes
    document.querySelectorAll('input[name="job_type"]').forEach(cb => {
        cb.addEventListener('change', () => {
            const checked = document.querySelector('input[name="job_type"]:checked');
            currentFilters.job_type = checked ? checked.value : '';
            loadJobs(1);
        });
    });

    // Location filter
    const locInput = document.getElementById('filter-location');
    if (locInput) {
        locInput.addEventListener('input', debounce(() => {
            currentFilters.location = locInput.value;
            loadJobs(1);
        }, 400));
    }

    // Salary
    const salMin = document.getElementById('filter-salary-min');
    const salMax = document.getElementById('filter-salary-max');
    if (salMin) salMin.addEventListener('change', () => { currentFilters.salary_min = salMin.value; loadJobs(1); });
    if (salMax) salMax.addEventListener('change', () => { currentFilters.salary_max = salMax.value; loadJobs(1); });

    // Clear filters
    const clearBtn = document.getElementById('clear-filters');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            currentFilters = {};
            document.querySelectorAll('.filter-panel input').forEach(i => { i.value = ''; i.checked = false; });
            loadJobs(1);
        });
    }
}

function renderPagination() {
    const container = document.getElementById('pagination');
    if (!container || totalPages <= 1) { if (container) container.innerHTML = ''; return; }

    let html = `<button class="page-btn" onclick="loadJobs(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>←</button>`;
    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
            html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="loadJobs(${i})">${i}</button>`;
        } else if (i === currentPage - 2 || i === currentPage + 2) {
            html += `<span style="color: var(--text-muted);">...</span>`;
        }
    }
    html += `<button class="page-btn" onclick="loadJobs(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>→</button>`;
    container.innerHTML = html;
}

function updateResultCount(count) {
    const el = document.getElementById('result-count');
    if (el) el.textContent = `${count} job${count !== 1 ? 's' : ''} found`;
}
