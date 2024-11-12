from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment, Task, TaskStatus, TaskStatusHistory
from .serializers import (
    CommentSerializer,
    TaskSerializer,
    TaskStatusHistorySerializer,
)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer: TaskSerializer):
        with transaction.atomic():
            task: Task = serializer.save()
            task.set_status(TaskStatus.CREATED, self.request.user)

        return task


class TaskStatusHistoryViewSet(viewsets.ModelViewSet):
    queryset = TaskStatusHistory.objects.all()
    serializer_class = TaskStatusHistorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer: TaskStatusHistorySerializer):
        with transaction.atomic():
            task_status_history: TaskStatusHistory = serializer.save()
            task_status_history.task.set_status(
                task_status_history.status, task_status_history.user, False
            )
            if task_status_history.status in (
                TaskStatus.IN_PROCESS,  # executor set
                TaskStatus.REVIEWED,  # work reviewed
            ):
                # Notify, for example to telegram or email
                # Example implementation: https://github.com/Demianight/rl_chat/blob/main/rl_chat/tasks.py
                # Example usage: https://github.com/Demianight/rl_chat/blob/2f9069d1169903d0e3b653a807a337af270cd0b3/apps/messages/routers.py#L52
                # Not same interface and message text obviously
                pass

        return task_status_history


class CommentsOnTaskViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_task(self):
        """Retrieve the task instance based on task_pk, raising 404 if not found."""
        task_id = self.kwargs["task_pk"]
        return get_object_or_404(Task, id=task_id)

    def get_queryset(self):
        return Comment.objects.filter(task=self.get_task())

    def perform_create(self, serializer: CommentSerializer):
        return serializer.save(user=self.request.user, task=self.get_task())


# Feels dumb to have two viewsets for slightly different actions
# But nesting deleting after tasks feels more dumb
class CommentsDeleteViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
