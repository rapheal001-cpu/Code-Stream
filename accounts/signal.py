# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Wallet
from .tasks import send_welcome_email

@receiver(post_save, sender=User)
def create_instructor_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.get_or_create(user=instance)
        send_welcome_email.delay(instance.email)