from django.contrib import admin
from django.urls import path, include, re_path

from task.views import TaskAPIList, TaskAPIUpdate, TaskAPIDetailView, TaskAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('task.urls')),
    path('user/', include('user.urls')),
    path('api/v1/restauth/', include('rest_framework.urls')),  # +login or logout
    path('api/v1/tasks/', TaskAPIView.as_view()),  # ../?status=1 вид запиту
    path('api/v1/tasklist/', TaskAPIList.as_view()),
    path('api/v1/tasklist/<int:pk>/', TaskAPIUpdate.as_view()),  # we can edit task, need enter task_id
    path('api/v1/taskdetail/<int:pk>/', TaskAPIDetailView.as_view()),  # we can edit and delete
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
