"""
GraphQL queries for Todo app.
"""

import graphene
from oauth2_provider.decorators import protected_resource
from .types import TodoType, UserType
from todos.models import Todo
from django.contrib.auth import get_user_model

User = get_user_model()

class Query(graphene.ObjectType):
    todos = graphene.List(TodoType)
    todo = graphene.Field(TodoType, id=graphene.ID(required=True))
    me = graphene.Field(UserType)

    @protected_resource()
    def resolve_todos(self, info):
        return Todo.objects.filter(user=info.context.user)

    @protected_resource()
    def resolve_todo(self, info, id):
        return Todo.objects.get(id=id, user=info.context.user)

    @protected_resource()
    def resolve_me(self, info):
        return info.context.user 