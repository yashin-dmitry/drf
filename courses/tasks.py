from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Subscription

User = get_user_model()

@shared_task
def send_course_update_email(course_id, update_message):
    subscriptions = Subscription.objects.filter(course_id=course_id)
    for subscription in subscriptions:
        user = subscription.user
        send_mail(
            'Обновление курса',
            update_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

@shared_task
def check_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    inactive_users.update(is_active=False)
