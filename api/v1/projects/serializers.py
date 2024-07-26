from rest_framework import serializers
from projects.models import Project, Task, Milestone, Notification, UserNotification


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'project', 'assignee']

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ['id', 'title', 'description', 'due_date', 'project']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'timestamp']

class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ['id', 'user', 'notification', 'is_read']
