from django.urls import path
from .views import CoursePaymentCheckoutSession
from .webhook import my_webhook_view

app_name = "payment"

urlpatterns = [
    path(
        "course/<int:course_id>/", CoursePaymentCheckoutSession.as_view(), name="course"
    ),
    path('stripe/webhook/', my_webhook_view, name='webhook')
]
