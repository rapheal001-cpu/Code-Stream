from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from .models import User
from django.template.loader import render_to_string
from django.conf import settings


@receiver(post_save, sender=User)
def signal_for_new_user(sender, instance, created, **kwargs):
    if created:
        # Immediately send user an email of a new user
        site_url = f'http://127.0.0.1:8000/'
        context = {"user": instance, 'site_url': site_url}
        subject_txt = render_to_string(
            "accounts/user/email/subject/welcome_email_subject.txt"
        )
        body_html = render_to_string(
            "accounts/user/email/html/welcome_email.html", context
        )
        email = EmailMessage(
            subject=subject_txt,
            body=body_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.email],
        )
        email.content_subtype = "html"
        email.send(fail_silently=True)
