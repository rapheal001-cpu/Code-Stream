from accounts.models import Notification
from celery import shared_task
from cloudinary.utils import cloudinary_url
from course.models import CourseVideo
from moviepy import VideoFileClip


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

    clip = VideoFileClip(video_public_id)
    duration = int(clip.duration)

    hours = duration // 3600
    minutes = duration % 3600
    seconds = (duration % 3600) % 60


    thumbnail_url, options = cloudinary_url(
        video_public_id,
        resource_type='video',
        format='jpg',
        transformation=[
            {'width': 400, 'crop': 'scale'},
            {'start_offset': 1, 'end_offset': 5},
        ]
    )

    video_instance.duration = duration
    video_instance.formatted_duration = f'{hours:02}:{minutes:02}:{seconds:02}'
    video_instance.thumbnail = thumbnail_url
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

    instructor = course_video.instructor
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