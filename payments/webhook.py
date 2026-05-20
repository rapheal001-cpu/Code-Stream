from accounts.models import User, Notification, OrderHistory, Wallet
from course.models import Course, Enrollment
import stripe
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


stripe_webhook_key = settings.STRIPE_WEBHOOK_SECRET_KEY


# WebHook
@csrf_exempt
def course_webhook(request):
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
        session = event["data"]["object"]

        course_id = session["metadata"]["course_id"]
        user_id = session["metadata"]["user_id"]

        course = get_object_or_404(Course, pk=course_id)
        user = get_object_or_404(User, pk=user_id)
        instructor = get_object_or_404(User, pk=course.instructor.pk)

        # Calculation
        course_price = course.price
        platform_cut = float(course.price) * 0.25
        instructor_earnings = int(course_price) - int(platform_cut)

        # Credit the Course Instructor and send notification
        if instructor.wallet is not None:
            wallet = get_object_or_404(Wallet, pk=instructor.wallet.pk)
            wallet.balance += instructor_earnings
            wallet.save()

            Notification.objects.create(
                user=instructor,
                name="New Course Purchase 🎉",
                message=(
                    f"Good news {instructor.full_name},\n\n"
                    f"Your course has just been purchased by @{user.username}.\n\n"
                    f"Course Details:\n"
                    f"• Course: {course.name}\n"
                    f"• Course Price: {course.price}\n"
                    f"• Student: @{user.username}\n\n"
                    f"• Date: {timezone.now()}\n\n"
                    f"Amount received: {instructor_earnings}"
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
            # Send Notification to the user(Student)
            Notification.objects.create(
                user=user,
                name="Course Purchase Successful 🎉",
                message=(
                    f"Congratulations {user.username},\n\n"
                    f"You have successfully purchased a course.\n\n"
                    f"Course Details:\n"
                    f"• Course: {course.name}\n"
                    f"• Course Instructor: @{course.instructor.username}\n"
                    f"• Amount Paid: {course.price}\n\n"
                    f"Thank you for learning with us!"
                ),
            )
            # Save User Order History
            OrderHistory.objects.create(
                user = user,
                name = 'Course Purchase',
                message = (
                    f"Congratulations {user.username},\n\n"
                    f"You have successfully purchased a course.\n\n"
                    f"Course Details:\n"
                    f"• Course: {course.name}\n"
                    f"• Course Instructor: @{course.instructor.username}\n"
                    f"• Amount Paid: {course.price}\n\n"
                    f"Thank you for learning with us!"
                ),
                status = 'success',
            )

    else:
        print(f"Unhandled event type: {event.type}")

    return HttpResponse(status=200)
