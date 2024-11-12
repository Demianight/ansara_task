from django.db import models

from users.models import User


class TaskStatus(models.TextChoices):
    CREATED = "created", "Created"
    IN_PROCESS = "in process", "In Process"
    COMPLETE = "complete", "Complete"
    REVIEWED = "reviewed", "Reviewed"


class Task(models.Model):
    description = models.TextField()
    current_status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.CREATED,
    )

    def set_status(
        self,
        status,
        user,
        should_history_be_created: bool = True,
    ):
        if status not in TaskStatus.values:
            raise ValueError("Invalid status")

        self.current_status = status
        self.save()

        if should_history_be_created:
            TaskStatusHistory.objects.create(
                task=self, status=status, user=user
            )

    def __str__(self):
        return f"Task {self.pk}: {self.description[:20]}..."


# Much better than multiple fields on Task model
# Allows adding and removing new statuses without changing Task model
class TaskStatusHistory(models.Model):
    task = models.ForeignKey(
        Task,
        related_name="status_history",
        on_delete=models.CASCADE,
    )
    status = models.CharField(max_length=20, choices=TaskStatus.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.pk} - {self.status} by {self.user.username} on {self.timestamp}"


class Comment(models.Model):
    """
    Allows some communication under task.
    Ask and answer questions, specify some requirements, etc.
    """

    task = models.ForeignKey(
        Task,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.pk} - {self.user.username} on {self.timestamp}"
