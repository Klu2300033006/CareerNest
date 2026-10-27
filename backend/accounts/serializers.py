"""
Serializers for user registration, authentication, and profile management.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Handles user registration with password confirmation."""

    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Validates login credentials."""

    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Full user profile serializer."""

    saved_jobs_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'phone', 'bio',
            'profile_picture', 'location', 'job_title',
            'is_staff', 'saved_jobs_count', 'created_at',
        ]
        read_only_fields = ['id', 'email', 'is_staff', 'created_at']

    def get_saved_jobs_count(self, obj):
        return obj.saved_jobs.count()


class UserUpdateSerializer(serializers.ModelSerializer):
    """Handles profile updates."""

    class Meta:
        model = User
        fields = ['full_name', 'phone', 'bio', 'profile_picture', 'location', 'job_title']
