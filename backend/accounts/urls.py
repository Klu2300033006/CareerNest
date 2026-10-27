"""
URL patterns for accounts app.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('save-job/<int:job_id>/', views.toggle_save_job, name='toggle_save_job'),
    path('saved-jobs/', views.saved_jobs_list, name='saved_jobs'),
]
