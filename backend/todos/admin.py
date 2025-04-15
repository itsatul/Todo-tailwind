"""
Admin configuration for the todos app.
"""

from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'completed', 'created_at', 'user')
    list_filter = ('completed', 'created_at', 'user')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
