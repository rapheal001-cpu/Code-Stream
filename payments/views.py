import stripe
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from course.models import Course
from django.views.generic import DetailView

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


class CoursePaymentCheckoutSession(LoginRequiredMixin, View):
    def get(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, pk=course_id)
        user = request.user

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(course.price) * 100,
                        "product_data": {
                            "name": course.name,
                            "images": [
                                request.build_absolute_uri(course.thumbnail.url)
                            ],
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            metadata={
                "course_id": course_id,
                "user_id": user.id,
            },
            success_url=f"http://localhost:8000/payment/checkout-course-success/{course.pk}/",
            cancel_url=f"http://localhost:8000/payment/checkout-course-cancel/{course.pk}/",
        )
        return redirect(session.url)

course_payment_checkout_session = CoursePaymentCheckoutSession.as_view()


class CourseCheckoutSuccessView(LoginRequiredMixin, DetailView):
    model = Course
    pk_field = "pk"
    pk_url_kwarg = "pk"
    context_object_name = "course"
    template_name = "payments/course_payment_success.html"

course_checkout_success_view = CourseCheckoutSuccessView.as_view()


class CourseCheckoutCancelView(LoginRequiredMixin, DetailView):
    model = Course
    pk_field = "pk"
    pk_url_kwarg = "pk"
    context_object_name = "course"
    template_name = "payments/course_payment_cancel.html"

course_checkout_cancel_view = CourseCheckoutCancelView.as_view()
