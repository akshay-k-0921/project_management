from django.db import models

from core.models import BaseModel
from users.models import CustomUser

# Create your models here.

# Project model
class Project(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.base_data(request)
        super().save(*args, **kwargs)


# Task model
class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')])
    due_date = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.base_data(request)
        super().save(*args, **kwargs)

# Milestone model
class Milestone(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')

    class Meta:
        verbose_name = 'Milestone'
        verbose_name_plural = 'Milestones'
        ordering = ['-date_added']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.base_data(request)
        super().save(*args, **kwargs)


# Notification model
class Notification(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.subject}"
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-date_added']

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.base_data(request)
        super().save(*args, **kwargs)

