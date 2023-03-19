from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('task/<int:task_id>', ShowTask.as_view(), name='task'),
    path('add_task/', add_task, name='add_task'),
    path('status/<int:status_id>/', show_status, name='status'),
]
