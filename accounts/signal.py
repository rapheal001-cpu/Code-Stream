from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .tasks import send_welcome_email


@receiver(post_save, sender=User)
def signal_for_new_user(sender, instance, created, **kwargs):
    if created:
        # Immediately send task to celery
        send_welcome_email.delay(instance.email)