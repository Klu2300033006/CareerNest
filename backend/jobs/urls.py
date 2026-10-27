"""
URL patterns for jobs app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('companies/', views.CompanyListView.as_view(), name='company_list'),
    path('public-stats/', views.public_stats, name='public_stats'),

    # Jobs
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job_create'),
    path('jobs/<int:pk>/update/', views.JobUpdateView.as_view(), name='job_update'),
    path('jobs/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),

    # Applications
    path('applications/', views.ApplicationCreateView.as_view(), name='application_create'),
    path('applications/history/', views.ApplicationListView.as_view(), name='application_list'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/<int:pk>/status/', views.ApplicationStatusUpdateView.as_view(), name='application_status'),

    # Stats
    path('stats/', views.user_stats, name='user_stats'),

    # Admin
    path('admin/applications/', views.AdminApplicationListView.as_view(), name='admin_applications'),
    path('admin/stats/', views.admin_stats, name='admin_stats'),
]
