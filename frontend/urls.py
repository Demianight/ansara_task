from django.urls import path
from .views import index, tasks

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", tasks, name="tasks"),
]
