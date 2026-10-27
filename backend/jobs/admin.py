"""
Admin registration for Job portal models.
"""

from django.contrib import admin
from .models import Category, Company, Job, Application


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'job_count')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'industry')
    search_fields = ('name', 'location')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'location', 'is_active', 'created_at')
    list_filter = ('job_type', 'experience_level', 'is_active', 'is_featured', 'category')
    search_fields = ('title', 'company__name', 'description')
    date_hierarchy = 'created_at'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('user__full_name', 'user__email', 'job__title')
    date_hierarchy = 'applied_at'
