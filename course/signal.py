from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Course
from accounts.models import Notification


@receiver(post_save, sender=Course)
def course_created(sender, instance, created, **kwargs):
    if created:
      Notification.objects.create(
        user=instance.instructor,
        name="Course Created complete",
        message=f"Great news! Your course \"{instance.name}\" is half way to publish.\n\n" "Next step: add your content and structure your lessons to create a great learning experience.\n\nNote: Once you publish you course you can not undo it.",
      )

@receiver(post_delete, sender=Course)
def course_deleted(sender, instance, **kwargs):
  if instance:
    Notification.objects.create(
      user=instance.instructor,
      name="Course Deleted",
      message=f"Your course \"{instance.name}\" has been deleted.",
    )