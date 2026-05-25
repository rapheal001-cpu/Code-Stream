from accounts.models import Notification
from celery import shared_task
from cloudinary.utils import cloudinary_url
from course.models import Course, CourseVideo


# =============================
#  Process Course Creation Data
# =============================
@shared_task(name="Process Course Creation Data", max_retries=3)
def process_course_creation_task(user, name, description, thumbnail, price, youtube_link, github_link, is_paid):
    Course.objects.create(
        instructor=user,
        name=name,
        description=description,
        thumbnail=thumbnail,
        price=price,
        youtube_link=youtube_link,
        github_link=github_link,
        is_paid=is_paid
    )
    return f"Course created successfully: {name}"


# =============================
#  Process Update Course Data
# =============================
def process_update_course_task(course_id, user, name, thumbnail, description, youtube_link, github_link):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return f"Course {course_id} does not exist."

    course.name = name
    course.description = description
    course.thumbnail = thumbnail
    course.description = description
    course.youtube_link = youtube_link
    course.github_link = github_link
    course.save()

    return f"Course ({course_id}) updated successfully: {name}"


# =============================================
#  Generate Thumbnail Url and Set Video duration
# ==============================================
@shared_task(name='Generate Course Video Thumbnail Url', max_retries=3)
def generate_thumbnail_task(course_video_id):
    try:
        video_instance = CourseVideo.objects.get(id=course_video_id)
    except CourseVideo.DoesNotExist:
        return f"Video {course_video_id} does not exist."

    video_public_id = video_instance.video.public_id

    thumbnail_url, options = cloudinary_url(
        video_public_id,
        resource_type='video',
        format='jpg',
        transformation=[
            {'width': 400, 'crop': 'scale'},
            {'start_offset': 1, 'end_offset': 5},
        ]
    )

    video_instance.thumbnail_url = thumbnail_url
    video_instance.save()

    return f"Thumbnail generated successfully: {thumbnail_url}"


# ====================================================
#  Send User Notification When Course Video Is Created
# ====================================================
@shared_task(name='Send User Notification When Course Video is Created', max_retries=3)
def send_user_notification_task(course_video_id):
    try:
        course_video = CourseVideo.objects.get(id=course_video_id)
    except CourseVideo.DoesNotExist:
        return f"Video {course_video_id} does not exist."

    instructor = course_video.course.instructor
    course = course_video.course

    Notification(
        user=instructor,
        name="Course Video Created",
        message=(
            f"You created a course video {instructor.username}."
            f"Video Detail:"
            f"Course: {course.name}"
            f"Video Name: {course_video.name}"
            f"Created: {course_video.created_at}"
        )
    )
    return f"Course Video created successfully: {course_video.name}"