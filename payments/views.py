import stripe
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from course.models import Course


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


class CoursePaymentCheckoutSession(LoginRequiredMixin, View):
    def get(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, pk=course_id)
        user = request.user
        YOUR_DOMAIN = f"{request.scheme}://{request.get_host()}/"

        session = stripe.checkout.Session.create(
            # payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(course.price) * 100,
                        "product_data": {
                            "name": course.name,
                            "images": [course.thumbnail],
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
            success_url=YOUR_DOMAIN + "paymentsuccess/",
            cancel_url=YOUR_DOMAIN + "cancel/",
        )
        return redirect(session.url)
