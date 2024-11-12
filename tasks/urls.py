from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from .views import (
    CommentsDeleteViewSet,
    CommentsOnTaskViewSet,
    TaskStatusHistoryViewSet,
    TaskViewSet,
)

router = routers.DefaultRouter()

router.register("tasks", TaskViewSet)
router.register("task_status_history", TaskStatusHistoryViewSet)
router.register("comments", CommentsDeleteViewSet)

comments_router = NestedSimpleRouter(router, "tasks", lookup="task")
comments_router.register(
    "comments", CommentsOnTaskViewSet, basename="task-comments"
)

urlpatterns = [
    *router.urls,
    *comments_router.urls,
]
