"""
GraphQL mutations for Todo app.
"""

import graphene
from oauth2_provider.decorators import protected_resource
from .types import TodoType
from todos.models import Todo

class CreateTodo(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        completed = graphene.Boolean()

    todo = graphene.Field(TodoType)

    @protected_resource()
    def mutate(self, info, title, description=None, completed=False):
        todo = Todo.objects.create(
            title=title,
            description=description,
            completed=completed,
            user=info.context.user
        )
        return CreateTodo(todo=todo)

class UpdateTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        completed = graphene.Boolean()

    todo = graphene.Field(TodoType)

    @protected_resource()
    def mutate(self, info, id, **kwargs):
        todo = Todo.objects.get(id=id, user=info.context.user)
        for key, value in kwargs.items():
            setattr(todo, key, value)
        todo.save()
        return UpdateTodo(todo=todo)

class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @protected_resource()
    def mutate(self, info, id):
        try:
            todo = Todo.objects.get(id=id, user=info.context.user)
            todo.delete()
            return DeleteTodo(success=True)
        except Todo.DoesNotExist:
            return DeleteTodo(success=False)

class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field() 