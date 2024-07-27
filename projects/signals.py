from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from projects.models import Milestone, Task, Notification
from .tasks import send_email_notification

User = get_user_model()

@receiver(post_save, sender=Task)
def task_created_or_updated(sender, instance, created, **kwargs):
    if created:
        subject = 'New Task Created'
        message = f'A new task "{instance.title}" has been created.'
    else:
        subject = 'Task Updated'
        message = f'The task "{instance.title}" has been updated.'

    # Create a notification for every user
    users = User.objects.all()
    for user in users:
        Notification.objects.create(user=user, subject=subject, message=message)

    send_email_notification.delay(subject, message)


@receiver(post_save, sender=Milestone)
def milestone_created_or_updated(sender, instance, created, **kwargs):
    if created:
        subject = 'New Milestone Created'
        message = f'A new milestone "{instance.title}" has been created.'
    else:
        subject = 'Milestone Updated'
        message = f'The milestone "{instance.title}" has been updated.'

    # Create a notification
    users = User.objects.all()
    for user in users:
        Notification.objects.create(user=user, subject=subject, message=message)

    send_email_notification.delay(subject, message)