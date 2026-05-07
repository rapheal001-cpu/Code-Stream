from accounts.models import User, Notification
from course.models import Course, Enrollment
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


stripe_webhook_key = settings.STRIPE_WEBHOOK_SECRET_KEY


# WebHook
@csrf_exempt
def webhook_view(request):
    event = None
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, stripe_webhook_key)
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event["type"] == "checkout.session.completed":
        payment_intent = event["data"]["object"]

        course_id = payment_intent["metadata"]["course_id"]
        user_id = payment_intent["metadata"]["user_id"]

        course = get_object_or_404(Course, pk=course_id)
        user = get_object_or_404(User, pk=user_id)
        instructor = get_object_or_404(User, pk=course.instructor.pk)

        # Credit the Course Instructor and send notification
        if instructor.wallet:
            instructor.wallet.balance += course.price
            instructor.wallet.save()
            Notification.objects.create(
                user=instructor,
                title="New Course Purchase 🎉",
                message=(
                    f"Good news {instructor.full_name},\n\n"
                    f"Your course has just been purchased by @{user.username}.\n\n"
                    f"Course Details:\n"
                    f"• Course: {course.name}\n"
                    f"• Price: {course.price}\n"
                    f"• Student: @{user.username}\n\n"
                    f"Amount received: {course.price}"
                ),
            )
        # Enroll The User to the course
        if user is not None:
            Enrollment.objects.get_or_create(
                user=user,
                course=course,
                amount_paid=course.price,
                is_paid=True,
            )
            # Send Notification to the user
            Notification.objects.create(
                user=user,
                title="Course Purchase Successful 🎉",
                message=(
                    f"Congratulations {user.username},\n\n"
                    f"You have successfully purchased a course.\n\n"
                    f"Course Details:\n"
                    f"• Course: {course.name}\n"
                    f"• Instructor: @{course.instructor.username}\n"
                    f"• Amount Paid: {course.price}\n\n"
                    f"Thank you for learning with us!"
                ),
            )

    else:
        print(f"Unhandled event type: {event.type}")

    return HttpResponse(status=200)
