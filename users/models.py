import uuid

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

from core.models import base_data

# User model with roles
class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=[
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('member', 'Member'),
    ], default='member')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group,related_name='custom_users', blank=True)
    user_permissions = models.ManyToManyField(Permission,related_name='custom_users', blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def __str__(self):
       return self.name

    def save(self, request=None, *args, **kwargs):
       base_data(self,request)
      
       super(CustomUser, self).save(*args, **kwargs)


# Project model
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, request=None, *args, **kwargs):
       base_data(self,request)
      
       super(Project, self).save(*args, **kwargs)



# Task model
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')])
    due_date = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='tasks')

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def save(self, request=None, *args, **kwargs):
       base_data(self,request)

       super(Task, self).save(*args, **kwargs)

# Milestone model
class Milestone(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')

    class Meta:
        verbose_name = 'Milestone'
        verbose_name_plural = 'Milestones'
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def save(self, request=None, *args, **kwargs):
       base_data(self,request)
      
       super(Milestone, self).save(*args, **kwargs)

# Notification model
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-timestamp']

    def __str__(self):
        return self.message

    def save(self, request=None, *args, **kwargs):
       base_data(self,request)
      
       super(Notification, self).save(*args, **kwargs)
