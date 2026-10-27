"""
Serializers for Job, Company, Category, and Application models.
"""

from rest_framework import serializers
from .models import Category, Company, Job, Application


class CategorySerializer(serializers.ModelSerializer):
    job_count = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'job_count']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'logo', 'website', 'description',
            'location', 'industry', 'employee_count', 'founded_year',
        ]


class JobListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for job listings."""

    company = CompanySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    application_count = serializers.ReadOnlyField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'category', 'salary_min',
            'salary_max', 'location', 'job_type', 'experience_level',
            'is_featured', 'application_count', 'is_saved',
            'created_at', 'deadline',
        ]

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.saved_by.filter(id=request.user.id).exists()
        return False


class JobDetailSerializer(serializers.ModelSerializer):
    """Full detail serializer for a single job."""

    company = CompanySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    application_count = serializers.ReadOnlyField()
    is_saved = serializers.SerializerMethodField()
    has_applied = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.saved_by.filter(id=request.user.id).exists()
        return False

    def get_has_applied(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Application.objects.filter(user=request.user, job=obj).exists()
        return False


class JobCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for admin to create/update jobs."""

    class Meta:
        model = Job
        fields = [
            'title', 'company', 'category', 'description',
            'requirements', 'responsibilities', 'salary_min',
            'salary_max', 'location', 'job_type', 'experience_level',
            'skills', 'is_active', 'is_featured', 'deadline',
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for job applications with nested job details."""

    job = JobListSerializer(read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'user', 'user_name', 'user_email', 'job',
            'resume', 'cover_letter', 'status',
            'applied_at', 'updated_at',
        ]
        read_only_fields = ['id', 'user', 'status', 'applied_at', 'updated_at']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for submitting an application."""

    class Meta:
        model = Application
        fields = ['job', 'resume', 'cover_letter']

    def validate(self, attrs):
        request = self.context['request']
        if Application.objects.filter(user=request.user, job=attrs['job']).exists():
            raise serializers.ValidationError('You have already applied for this job.')
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ApplicationStatusSerializer(serializers.ModelSerializer):
    """Admin serializer to update application status."""

    class Meta:
        model = Application
        fields = ['status']
