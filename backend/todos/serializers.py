"""
Serializers for the todos app.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TodoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Todo model.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'user']
        read_only_fields = ['created_at', 'user']

    def validate_title(self, value):
        """
        Validate the title field.
        """
        logger.info(f"Validating title: {value}")
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip()

    def create(self, validated_data):
        """
        Create and return a new `Todo` instance, given the validated data.
        """
        logger.info(f"Creating todo with validated data: {validated_data}")
        return super().create(validated_data) 