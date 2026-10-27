/**
 * CareerNest — Job Detail & Apply Page Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    loadJobDetail();
});

async function loadJobDetail() {
    const params = new URLSearchParams(window.location.search);
    const jobId = params.get('id');
    if (!jobId) { window.location.href = 'jobs.html'; return; }

    try {
        const job = await api.request(`/jobs/${jobId}/`, 'GET');
        renderJobDetail(job);
        initApplyForm(job);
    } catch (e) {
        document.getElementById('job-detail-container').innerHTML =
            '<div class="empty-state"><div class="empty-state-icon">😔</div><div class="empty-state-title">Job not found</div><a href="jobs.html" class="btn btn-primary btn-sm mt-4">Browse Jobs</a></div>';
    }
}

function renderJobDetail(job) {
    const company = job.company || {};
    const logo = company.name ? company.name[0] : '?';

    document.getElementById('jd-title').textContent = job.title;
    document.getElementById('jd-company').textContent = company.name || '';
    document.getElementById('jd-logo').textContent = logo;

    const badgesEl = document.getElementById('jd-badges');
    if (badgesEl) {
        badgesEl.innerHTML = `
            <span class="badge badge-primary">${typeBadge(job.job_type)}</span>
            <span class="badge badge-neutral">${job.experience_level || 'Mid'} Level</span>
            <span class="badge badge-neutral">📍 ${job.location}</span>
        `;
    }

    // Description content
    const descEl = document.getElementById('jd-description');
    if (descEl) descEl.innerHTML = formatTextToHTML(job.description);

    const reqEl = document.getElementById('jd-requirements');
    if (reqEl) reqEl.innerHTML = formatTextToHTML(job.requirements);

    const respEl = document.getElementById('jd-responsibilities');
    if (respEl) respEl.innerHTML = formatTextToHTML(job.responsibilities);

    // Sidebar info
    const infoMap = {
        'jd-salary': formatSalary(job.salary_min, job.salary_max),
        'jd-location': job.location,
        'jd-type': typeBadge(job.job_type),
        'jd-experience': job.experience_level || 'N/A',
        'jd-posted': formatDate(job.created_at),
        'jd-deadline': job.deadline || 'Open',
        'jd-applicants': (job.application_count || 0) + ' applicants',
    };
    Object.entries(infoMap).forEach(([id, val]) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
    });

    // Company info
    const compNameEl = document.getElementById('jd-comp-name');
    if (compNameEl) compNameEl.textContent = company.name || '';
    const compDescEl = document.getElementById('jd-comp-desc');
    if (compDescEl) compDescEl.textContent = company.description || '';

    // If already applied
    if (job.has_applied) {
        const applySection = document.getElementById('apply-section');
        if (applySection) {
            applySection.innerHTML = '<div class="badge badge-success" style="padding:12px 20px;font-size:14px;">✓ You have already applied for this position</div>';
        }
    }

    // Tab switching
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
            tab.classList.add('active');
            const target = document.getElementById(tab.dataset.tab);
            if (target) target.style.display = 'block';
        });
    });
}

function initApplyForm(job) {
    const form = document.getElementById('apply-form');
    if (!form || job.has_applied) return;

    // File upload drag & drop
    const fileUpload = document.querySelector('.file-upload');
    const fileInput = document.getElementById('resume-file');
    const fileName = document.getElementById('file-name');

    if (fileUpload) {
        ['dragenter', 'dragover'].forEach(evt => {
            fileUpload.addEventListener(evt, (e) => { e.preventDefault(); fileUpload.classList.add('dragover'); });
        });
        ['dragleave', 'drop'].forEach(evt => {
            fileUpload.addEventListener(evt, (e) => { e.preventDefault(); fileUpload.classList.remove('dragover'); });
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', () => {
            if (fileInput.files[0]) {
                fileName.textContent = fileInput.files[0].name;
                fileName.style.color = 'var(--color-primary)';
            }
        });
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!requireAuth()) return;

        const resume = fileInput?.files[0];
        const coverLetter = document.getElementById('cover-letter')?.value || '';

        if (!resume) {
            showToast('Please upload your resume.', 'error');
            return;
        }

        const btn = form.querySelector('.btn-primary');
        btn.classList.add('btn-loading');
        btn.innerHTML = '<span class="btn-text">Submitting...</span>';

        const formData = new FormData();
        formData.append('job', job.id);
        formData.append('resume', resume);
        formData.append('cover_letter', coverLetter);

        try {
            await api.upload('/applications/', formData);
            // Show success modal
            const modal = document.getElementById('success-modal');
            if (modal) modal.classList.add('active');
            showToast('Application submitted successfully!', 'success');
        } catch (err) {
            const msg = err.data ? (typeof err.data === 'string' ? err.data : Object.values(err.data).flat().join(' ')) : 'Failed to submit application.';
            showToast(msg, 'error');
            btn.classList.remove('btn-loading');
            btn.innerHTML = 'Submit Application';
        }
    });
}

function formatTextToHTML(text) {
    if (!text) return '<p>No information provided.</p>';
    return text.split('\n').filter(l => l.trim()).map(line => {
        if (line.trim().startsWith('-') || line.trim().startsWith('•')) {
            return `<li>${line.replace(/^[-•]\s*/, '')}</li>`;
        }
        return `<p>${line}</p>`;
    }).join('').replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
}
