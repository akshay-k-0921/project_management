from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model


User = get_user_model()

@shared_task
def send_email_notification(subject, message):
     # Fetch all active users' email addresses
    recipient_list = list(User.objects.filter(is_active=True).values_list('email', flat=True))
    
    send_mail(
        subject,
        message,
        'k03774393@gmail.com',
        recipient_list,
        fail_silently=False,
    )