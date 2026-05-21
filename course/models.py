from datetime import timedelta
from cloudinary.models import CloudinaryField
from django.db import models
from accounts.models import User
from django.db.models import Sum
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal
from django.urls import reverse


class Course(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_instructor", verbose_name="Course Instructor")
    name = models.CharField(max_length=255, verbose_name="Course Name")
    slug = models.SlugField(unique=True, verbose_name="Course Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Course Description")
    thumbnail = CloudinaryField(resource_type='image', folder='course/thumbnails/', verbose_name="Course Thumbnail")
    price = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"), verbose_name="Course Price")
    students = models.ManyToManyField(User, through="Enrollment", related_name="enrolled_courses", blank=True, verbose_name="Course Students")
    views = models.ManyToManyField(User, blank=True, verbose_name="Course Views", related_name="course_views")
    likes = models.ManyToManyField(User, blank=True, verbose_name="Course Likes", related_name="course_likes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Updated at")

    def get_absolute_url(self):
        return reverse("course-detail-view", kwargs={"slug": self.slug})

    @property
    def is_updated(self):
        return self.updated_at != self.created_at

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.instructor})'


    def course_videos(self):
        return self.videos.all()

    @property
    def total_videos(self):
        return self.videos.count() if hasattr(self, "videos") else 0

    @property
    def total_students(self):
        return self.students.count()

    @property
    def total_views(self):
        return self.views.count()

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def is_new(self):
        return self.created_at  > timezone.now() - timedelta(days=1)

    @property
    def total_videos_duration(self):
        result = self.videos.aggregate(total=Sum("duration"))
        total = result["total"] or 0  # Handle None

        days = total // 86400
        remainder = total % 86400  # What's left after days

        hours = remainder // 3600
        remainder = remainder % 3600  # What's left after hours

        minutes = remainder // 60
        seconds = remainder % 60  # What's left after minutes

        return f"{days}d {hours}h {minutes}m {seconds}s"


class CourseVideo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="videos", verbose_name="Course")
    name = models.CharField(max_length=255, verbose_name="Video Name")
    description = models.TextField(blank=True, null=True, verbose_name="Video Description")
    duration = models.PositiveIntegerField(default=0, verbose_name="Video Duration")
    formatted_duration = models.CharField(max_length=100, verbose_name="Formatted Video Duration")
    video = CloudinaryField(resource_type='video', folder='course/videos/', verbose_name="Course Video File")
    thumbnail = CloudinaryField(resource_type='image', folder='course/video_thumbnails/', verbose_name="Course Video Thumbnail")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")



    class Meta:
        ordering = ["created_at"]
        verbose_name = "Course Video"
        verbose_name_plural = "Course Videos"

    def __str__(self):
        return f"{self.course.name}  ({self.name})"


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_enrollment", verbose_name="Enrolled User")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_enrollment", verbose_name="Course")
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    is_paid = models.BooleanField(default=False, verbose_name="Is Paid")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Enrolled At")

    class Meta:
        ordering = ["-enrolled_at"]
        verbose_name = "Course Enrollment"
        verbose_name_plural = "Course Enrollments"
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user} ({self.course.name})"


class ShortVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="public_video", verbose_name="User")
    name = models.CharField(max_length=225, verbose_name="Short Video Name")
    slug = models.SlugField(unique=True, verbose_name="Short Video Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Short Video Description")
    video = CloudinaryField(resource_type='video', folder='short_video/videos/', verbose_name="Short Video File")
    thumbnail = CloudinaryField(resource_type='image', folder='short_video/thumbnails/', verbose_name="Short Video Thumbnail")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    def get_absolute_url(self):
        return reverse("short-video-detail-view", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Short Video"
        verbose_name_plural = "Short Videos"

    def __str__(self):
        return f"{self.user} ({self.name})"