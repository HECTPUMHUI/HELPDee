from django.urls import path

from .views import *

urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('task/<int:task_id>', ShowTask.as_view(), name='task'),
    path('task/<int:task_id>/add_comment/', add_comment, name='add_comment'),
    path('add_task/', add_task, name='add_task'),
    path('status/<int:status_id>/', show_status, name='status'),
    path('task/<int:task_id>/accept/', task_accept, name='task_accept'),
    path('task/<int:task_id>/reject/', task_reject, name='task_reject'),
    path('task/<int:task_id>/restore/', task_restore, name='task_restore'),
    path('tasks/restore/', RestoreTaskList.as_view(), name='restored_tasks'),
    path('task/<int:task_id>/edit/', edit_task, name='edit_task'),
]
