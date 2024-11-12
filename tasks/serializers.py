from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer

from .models import Task, TaskStatusHistory, Comment


class TaskStatusHistorySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(),
        write_only=True,
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = TaskStatusHistory
        fields = ("id", "task", "status", "user_id", "user", "timestamp")
        extra_kwargs = {
            "task": {"write_only": True},
            "user_id": {"write_only": True},
            "user": {"read_only": True},
        }

    # OPTIONAL, good in Task representation but looks a bit dumb in personal view
    # To show status info under "status code"
    # Maybe a bit too "hardcoded", haven't found simpler solution
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            instance.status: {
                "id": representation["id"],
                "user": representation["user"],
                "timestamp": representation["timestamp"],
            }
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "task_id",
            "user_id",
            "text",
            "timestamp",
        )
        extra_kwargs = {
            "user_id": {"read_only": True},
        }


class TaskSerializer(serializers.ModelSerializer):
    status_history = TaskStatusHistorySerializer(many=True, read_only=True)
    comments = CommentSerializer(
        many=True, read_only=True
    )  # Can be hidden due to size of serializer

    class Meta:
        model = Task
        fields = (
            "id",
            "description",
            "current_status",
            "status_history",
            "comments",
        )
        extra_kwargs = {
            "status_history": {"read_only": True},
        }
