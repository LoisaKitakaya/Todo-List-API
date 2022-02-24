from django.contrib import admin
from .models import TodoList

# Register your models here.
class TodoListAdmin(admin.ModelAdmin):

    list_display = ('owner', 'thing_to_do', 'completed', 'created_on')
    list_filter = ('owner', 'completed', 'created_on')

admin.site.register(TodoList, TodoListAdmin)
