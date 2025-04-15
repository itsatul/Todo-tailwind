"""
Views for the todos app.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Todo
from .serializers import TodoSerializer, UserSerializer
import logging

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class TodoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing todos.
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return todos for the current user.
        """
        logger.info(f"Getting todos for user: {self.request.user}")
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new todo.
        """
        logger.info(f"Creating todo with data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(f"Successfully created todo: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        Set the user field when creating a new todo.
        """
        logger.info(f"Setting user for todo: {self.request.user}")
        serializer.save(user=self.request.user) 