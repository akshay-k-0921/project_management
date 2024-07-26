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

