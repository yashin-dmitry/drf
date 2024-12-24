from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription

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
