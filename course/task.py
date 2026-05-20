from celery import shared_task
from django.core.files import File
from .models import CourseVideo
from moviepy import VideoFileClip
import os


@shared_task
def generate_thumbnail_course_video(course_video_id):
    try:
        course_video = CourseVideo.objects.get(id=course_video_id)
    except CourseVideo.DoesNotExist:
        return "Course video not found"

    video_path = course_video.video.path

    video = VideoFileClip(video_path)

    # Duration
    duration = int(video.duration)

    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60

    course_video.duration = duration
    course_video.formatted_duration = (
        f"{hours:02}:{minutes:02}:{seconds:02}"
    )

    # Thumbnail path
    thumbnail_path = (
        f"{os.path.splitext(video_path)[0]}_thumbnail.png"
    )

    # Save frame at 5 seconds
    video.save_frame(thumbnail_path, t=5)

    # Save thumbnail to model
    with open(thumbnail_path, "rb") as file:
        course_video.thumbnail.save(
            os.path.basename(thumbnail_path),
            File(file),
            save=False
        )

    course_video.save()

    video.close()
    return "Thumbnail saved"