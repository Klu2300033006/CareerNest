"""
API views for Jobs, Applications, Categories, Companies, and Stats.
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Count, Q

from .models import Category, Company, Job, Application
from .serializers import (
    CategorySerializer,
    CompanySerializer,
    JobListSerializer,
    JobDetailSerializer,
    JobCreateUpdateSerializer,
    ApplicationSerializer,
    ApplicationCreateSerializer,
    ApplicationStatusSerializer,
)
from .filters import JobFilter


# ──────────────────────────────────────────────
# Category & Company endpoints
# ──────────────────────────────────────────────

class CategoryListView(generics.ListAPIView):
    """GET /api/categories/ — list all job categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class CompanyListView(generics.ListAPIView):
    """GET /api/companies/ — list all companies."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]
    pagination_class = None


# ──────────────────────────────────────────────
# Job endpoints
# ──────────────────────────────────────────────

class JobListView(generics.ListAPIView):
    """
    GET /api/jobs/
    Public job listing with search, filter, and pagination.
    """
    serializer_class = JobListSerializer
    permission_classes = [AllowAny]
    filterset_class = JobFilter
    search_fields = ['title', 'company__name', 'description', 'skills']
    ordering_fields = ['created_at', 'salary_min', 'salary_max', 'title']

    def get_queryset(self):
        return Job.objects.filter(
            is_active=True
        ).select_related('company', 'category')


class JobDetailView(generics.RetrieveAPIView):
    """GET /api/jobs/<id>/ — full job details."""
    queryset = Job.objects.select_related('company', 'category')
    serializer_class = JobDetailSerializer
    permission_classes = [AllowAny]


class JobCreateView(generics.CreateAPIView):
    """POST /api/jobs/create/ — admin creates a new job."""
    serializer_class = JobCreateUpdateSerializer
    permission_classes = [IsAdminUser]


class JobUpdateView(generics.UpdateAPIView):
    """PUT /api/jobs/<id>/update/ — admin updates a job."""
    queryset = Job.objects.all()
    serializer_class = JobCreateUpdateSerializer
    permission_classes = [IsAdminUser]


class JobDeleteView(generics.DestroyAPIView):
    """DELETE /api/jobs/<id>/delete/ — admin deletes a job."""
    queryset = Job.objects.all()
    permission_classes = [IsAdminUser]


# ──────────────────────────────────────────────
# Application endpoints
# ──────────────────────────────────────────────

class ApplicationCreateView(generics.CreateAPIView):
    """POST /api/applications/ — user applies for a job."""
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated]


class ApplicationListView(generics.ListAPIView):
    """GET /api/applications/ — user's application history."""
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(
            user=self.request.user
        ).select_related('job__company', 'job__category')


class ApplicationDetailView(generics.RetrieveAPIView):
    """GET /api/applications/<id>/ — single application detail."""
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Application.objects.all()
        return Application.objects.filter(user=self.request.user)


class ApplicationStatusUpdateView(generics.UpdateAPIView):
    """PATCH /api/applications/<id>/status/ — admin updates status."""
    queryset = Application.objects.all()
    serializer_class = ApplicationStatusSerializer
    permission_classes = [IsAdminUser]


# ──────────────────────────────────────────────
# Admin — all applications
# ──────────────────────────────────────────────

class AdminApplicationListView(generics.ListAPIView):
    """GET /api/admin/applications/ — all applications (admin only)."""
    queryset = Application.objects.select_related(
        'user', 'job__company'
    ).all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['user__full_name', 'user__email', 'job__title']


# ──────────────────────────────────────────────
# Statistics
# ──────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """
    GET /api/stats/
    Dashboard statistics for the current user.
    """
    user = request.user
    applications = Application.objects.filter(user=user)

    return Response({
        'total_applications': applications.count(),
        'pending': applications.filter(status='pending').count(),
        'reviewed': applications.filter(status='reviewed').count(),
        'accepted': applications.filter(status='accepted').count(),
        'rejected': applications.filter(status='rejected').count(),
        'saved_jobs': user.saved_jobs.count(),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def public_stats(request):
    """
    GET /api/public-stats/
    Public landing page statistics.
    """
    return Response({
        'total_jobs': Job.objects.filter(is_active=True).count(),
        'total_companies': Company.objects.count(),
        'total_categories': Category.objects.count(),
        'total_applications': Application.objects.count(),
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    """
    GET /api/admin/stats/
    Admin dashboard analytics.
    """
    total_apps = Application.objects.count()
    accepted = Application.objects.filter(status='accepted').count()

    return Response({
        'total_jobs': Job.objects.count(),
        'active_jobs': Job.objects.filter(is_active=True).count(),
        'total_users': __import__('django.contrib.auth', fromlist=['get_user_model']).get_user_model().objects.count(),
        'total_applications': total_apps,
        'pending_applications': Application.objects.filter(status='pending').count(),
        'accepted_applications': accepted,
        'rejected_applications': Application.objects.filter(status='rejected').count(),
        'acceptance_rate': round((accepted / total_apps * 100), 1) if total_apps > 0 else 0,
        'jobs_by_type': list(
            Job.objects.values('job_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        ),
        'top_categories': list(
            Category.objects.annotate(
                count=Count('jobs', filter=Q(jobs__is_active=True))
            ).values('name', 'count').order_by('-count')[:6]
        ),
    })
