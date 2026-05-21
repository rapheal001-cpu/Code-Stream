from celery import shared_task
from .models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

# Send Welcome Email To User
@shared_task
def send_welcome_email(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return 'This user does not exist'

    site_url = f'http://localhost:8000/'
    context = {"user": user, 'site_url': site_url}
    subject_txt = render_to_string(
        "core/user/email/subject/welcome_email_subject.txt"
    )
    body_html = render_to_string(
        "core/user/email/html/welcome_email.html", context
    )
    email = EmailMessage(
        subject=subject_txt,
        body=body_html,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = "html"
    email.send(fail_silently=True)
    return "Welcome email sent"