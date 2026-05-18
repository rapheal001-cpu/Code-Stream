from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course
from accounts.models import Notification


@receiver(post_save, sender=Course)
def course_created(sender, instance, created, **kwargs):
    if created:
      Notification.objects.create(
    user=instance.instructor,
    name="Course setup complete",
    message=f"Great news! Your course \"{instance.name}\" is now live on your dashboard.\n\n"
        "Next step: add your content and structure your lessons to create a great learning experience.",
    )
