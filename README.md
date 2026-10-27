# 🏠 CareerNest — Job Portal

A modern, full-stack job portal application built with **Django REST Framework** and a handcrafted **HTML/CSS/JS** frontend.

![CareerNest](https://img.shields.io/badge/CareerNest-Job%20Portal-4F46E5?style=for-the-badge)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django)
![DRF](https://img.shields.io/badge/DRF-3.14-red?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

### For Job Seekers
- 🔍 **Browse & Search Jobs** — Filter by type, location, salary, experience level
- 📝 **One-Click Apply** — Resume upload with drag-and-drop + cover letter
- 📊 **Dashboard** — Track all applications with real-time status updates
- 📋 **Application History** — Filter by status (Pending / Reviewed / Accepted / Rejected)

### For Admins
- 🏢 **Company & Job Management** — Full CRUD for job listings
- 👥 **Application Review** — Update application statuses with dropdown controls
- 📈 **Analytics Dashboard** — Overview stats for jobs, users, and applications

### General
- 🔐 **JWT Authentication** — Secure login/register with token refresh
- 🌗 **Dark/Light Mode** — Theme toggle with persistence
- 📱 **Fully Responsive** — Works on desktop, tablet, and mobile
- 🎨 **Modern UI** — Glassmorphism, smooth animations, custom design system

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, Django 4.2, Django REST Framework |
| **Authentication** | Simple JWT (Access + Refresh tokens) |
| **Database** | SQLite (dev) / PostgreSQL (prod-ready) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Design** | Custom CSS Variables, Glassmorphism, CSS Grid/Flexbox |
| **API** | RESTful, with filtering via `django-filter` |

---

## 📁 Project Structure

```
CareerNest/
├── backend/
│   ├── careernest/          # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── accounts/            # User authentication app
│   │   ├── models.py        # Custom User model
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── jobs/                # Job listings app
│   │   ├── models.py        # Category, Company, Job, Application
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── filters.py
│   │   └── management/commands/seed_data.py
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── index.html           # Landing page
    ├── login.html           # Login page
    ├── register.html        # Registration page
    ├── dashboard.html       # User dashboard
    ├── jobs.html            # Job listings
    ├── job-detail.html      # Job detail + apply
    ├── applications.html    # Application history
    ├── admin-panel.html     # Admin management
    ├── css/                 # Stylesheets
    └── js/                  # JavaScript modules
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/CareerNest.git
cd CareerNest
```

### 2. Set up the backend
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data    # Seeds 8 categories, 8 companies, 16 jobs
python manage.py runserver 8000
```

### 3. Start the frontend
```bash
cd frontend
python -m http.server 3000
```

### 4. Open in browser
Navigate to **http://localhost:3000**

---

## 🔑 Demo Accounts

| Role | Email | Password |
|---|---|---|
| **Job Seeker** | `demo@careernest.com` | `demo1234` |
| **Admin** | `admin@careernest.com` | `admin1234` |

---

## 📡 API Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/auth/register/` | POST | ❌ | Register new user |
| `/api/auth/login/` | POST | ❌ | Get JWT tokens |
| `/api/auth/token/refresh/` | POST | ❌ | Refresh access token |
| `/api/auth/profile/` | GET/PUT | ✅ | User profile |
| `/api/jobs/` | GET | ❌ | List jobs (filterable) |
| `/api/jobs/<id>/` | GET | ❌ | Job detail |
| `/api/categories/` | GET | ❌ | List categories |
| `/api/companies/` | GET | ❌ | List companies |
| `/api/applications/` | POST | ✅ | Submit application |
| `/api/applications/history/` | GET | ✅ | User's applications |
| `/api/stats/` | GET | ✅ | Dashboard stats |
| `/api/public-stats/` | GET | ❌ | Landing page stats |

---

## 🎨 Design System

The UI uses a custom design system with:
- **CSS Custom Properties** for theming (light/dark)
- **Glassmorphism** cards with `backdrop-filter`
- **Consistent spacing** scale (4px base)
- **Inter font** for clean typography
- **Smooth animations** with `@keyframes` and CSS transitions

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ by <strong>Kusha</strong>
</p>
