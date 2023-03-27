from django.contrib import admin
from django.urls import path, include

from task.views import TaskAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('task.urls')),
    path('user/', include('user.urls')),
    path('api/v1/tasklist/', TaskAPIView.as_view(), name='task_list')
]
