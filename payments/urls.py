from django.urls import path
from .views import (
    CoursePaymentCheckoutSession,
    CourseCheckoutSuccessView,
    CourseCheckoutCancelView,
)
from .webhook import webhook_view

app_name = "payment"

urlpatterns = [
    path(
        "checkout-course/<int:course_id>/",
        CoursePaymentCheckoutSession.as_view(),
        name="checkout-course",
    ),
    path(
        "checkout-course-success/<int:pk>/",
        CourseCheckoutSuccessView.as_view(),
        name="checkout-course-success",
    ),
    path(
        "checkout-course-cancel/<int:pk>/",
        CourseCheckoutCancelView.as_view(),
        name="checkout-course-cancel",
    ),
    path("stripe/webhook/", webhook_view, name="webhook"),
]
