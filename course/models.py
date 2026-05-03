from django.db import models
from accounts.models import User
from django.utils.text import slugify
from decimal import Decimal
from django.urls import reverse


class Course(models.Model):
  instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_instructor")
  name = models.CharField(max_length=255)
  slug = models.SlugField(unique=True)
  description = models.TextField(blank=True, null=True)
  thumbnail = models.ImageField(upload_to="course/thumbnails/", default='course/thumbnails/default/default.png')
  price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
  students = models.ManyToManyField(User, through="Enrollment", related_name="enrolled_courses", blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ["-created_at"]
    verbose_name = "Course"
    verbose_name_plural = "Courses"

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    super().save(*args, **kwargs)

  def __str__(self):
    return self.name

  @property
  def total_videos(self):
    return self.videos.count() if hasattr(self, "videos") else 0

  @property
  def total_students(self):
    return self.students.count()

  def get_absolute_url(self):
    return reverse("course:course-detail", kwargs={"slug": self.slug})


class CourseVideo(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="videos")
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  video = models.FileField(upload_to="course/videos/")
  thumbnail = models.ImageField(upload_to="course/video_thumbs/", default='course/video_thumbs/default/default.png')
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ["-created_at"]
    verbose_name = "Course Video"
    verbose_name_plural = "Course Videos"

  def __str__(self):
    return f"{self.course.name} -> {self.title}"


class Enrollment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_enrollment")
  course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_enrollment")
  amount_paid = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
  is_paid = models.BooleanField(default=False)
  enrolled_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ["-enrolled_at"]
    verbose_name = "Course Enrollment"
    verbose_name_plural = "Course Enrollments"
    unique_together = ("user", "course")

  def __str__(self):
    return f"{self.user.username} → {self.course.name}"


class FreeCourseVideo(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='free_course_video_user')
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  video = models.FileField(upload_to="course/free_course/videos/")
  thumbnail = models.ImageField(upload_to="course/free_course/video_thumbs/", default='course/free_course/video_thumbs/default/default.png')
  created_at = models.DateTimeField(auto_now_add=True)
  
  def get_absolute_url(self):
    return reverse('video-detail', kwargs={'pk': self.pk})

  class Meta:
    ordering = ["-created_at"]
    verbose_name = "Free Course Video"
    verbose_name_plural = "Free Course Videos"

  def __str__(self):
    return f"{self.course.name} -> {self.title}"