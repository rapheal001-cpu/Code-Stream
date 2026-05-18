from django.urls import path
from .views import (
    course_payment_checkout_session,
    course_checkout_success_view,
    course_checkout_cancel_view,
)
from .webhook import course_webhook

urlpatterns = [
    path(
        "checkout-course/<int:course_id>/",
        course_payment_checkout_session,
        name="checkout-course-view",
    ),
    path(
        "checkout-course-success/<int:pk>/",
        course_checkout_success_view,
        name="checkout-course-success-view",
    ),
    path(
        "checkout-course-cancel/<int:pk>/",
        course_checkout_cancel_view,
        name="checkout-course-cancel-view",
    ),
    path("stripe/webhook/", course_webhook, name="webhook-view"),
]
