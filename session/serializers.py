from rest_framework import serializers
from .models import UserSession

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserSessionSerializer(serializers.ModelSerializer):
    """Serializer for session management"""
    class Meta:
        model = UserSession
        fields = '__all__'
        read_only_fields = ['session_id', 'is_open', 'created', 'updated', 'created_by']

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user list/retrieve operations"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']
 
 
class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for user creation with password validation"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
 
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
 
    def validate(self, data):
        """Validate that passwords match"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data
 
    def create(self, validated_data):
        """Create user and set password"""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
 
 
class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed user information"""
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
 

class MessangerLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    session_id = serializers.UUIDField(required=True)

class TaskStatusSerializer(serializers.Serializer):
    task_id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    result = serializers.JSONField(read_only=True, required=False)