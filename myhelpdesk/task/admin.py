from django.contrib import admin
from .models import Task, Status


@admin.register(Task)
class Task(admin.ModelAdmin):
    list_display = ['title', 'description', 'time_created', 'time_updated', 'process']


admin.site.register(Status)
