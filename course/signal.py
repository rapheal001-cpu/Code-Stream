from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course
from accounts.models import Notification

@receiver(post_save, sender=Course)
def course_created(sender, instance, created, **kwargs):
  if created:
    Notification.objects.create(user=instance.instructor, title='Course Created', message=f'Your course ({instance.name}) has been successfully created. \nYou can now add content and start engaging students.')