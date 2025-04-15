"""
GraphQL types for Todo app.
"""

from graphene_django import DjangoObjectType
from todos.models import Todo
from django.contrib.auth import get_user_model

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'todos')

class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed', 'created_at', 'user') 