from celery import shared_task
from .models import CourseVideo
from moviepy import VideoFileClip
import tempfile
import requests
import os
import cloudinary.uploader


@shared_task
def generate_thumbnail_course_video(course_video_id):
    try:
        course_video = CourseVideo.objects.get(id=course_video_id)

        video_url = course_video.video.url
        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")

        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                temp_video_file.write(chunk)

        temp_video_file.close()
        video_path = temp_video_file.name

        video = VideoFileClip(video_path)

        duration = int(video.duration)

        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60

        course_video.duration = duration
        course_video.formatted_duration = f'{hours:02}:{minutes:02}:{seconds:02}'

        thumbnail_path = os.path.splitext(video_path)[0] + "_thumbnail.png"


        video.save_frame(thumbnail_path, t=5)

        upload_result = cloudinary.uploader.upload(thumbnail_path)
        course_video.thumbnail = upload_result["secure_url"]
        course_video.save()

        # cleanup
        video.close()
        os.remove(video_path)
        os.remove(thumbnail_path)

        return "Thumbnail generated successfully"

    except Exception as e:
        return f"Error generating thumbnail\nError: {str(e)}"