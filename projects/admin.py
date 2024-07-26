from django.contrib import admin

from projects.models import Milestone, Notification, Project, Task, UserNotification

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name','description','owner']

admin.site.register(Project, ProjectAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title','description','status','due_date','assignee']

admin.site.register(Task, TaskAdmin)


class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title','description','due_date','project']

admin.site.register(Milestone, MilestoneAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user','message','timestamp']

admin.site.register(Notification, NotificationAdmin)


class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['user','notification','is_read']

admin.site.register(UserNotification, UserNotificationAdmin)