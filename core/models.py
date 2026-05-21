from django.db import models
from cloudinary.models import CloudinaryField
from accounts.models import User
from django.urls import reverse
from django.utils.text import slugify


# ========================================
#  Short Video (Access: Authenticated User)
# =========================================
class ShortVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="public_video", verbose_name="User")
    name = models.CharField(max_length=225, verbose_name="Short Video Name")
    slug = models.SlugField(unique=True, verbose_name="Short Video Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Short Video Description")
    video = CloudinaryField(resource_type='video', folder='short_video/videos/', verbose_name="Short Video File")
    thumbnail = models.URLField(unique=True, verbose_name="Short Video Thumbnail Url")
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


#=======
# Report
#=======
class Report(models.Model):
    user_identifier = models.CharField(max_length=50, verbose_name="User Identifier")
    topic = models.CharField(max_length=500, verbose_name="Topic")
    body = models.TextField(verbose_name="Body")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return f"{self.user_identifier} Report"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Report"
        verbose_name_plural = "Reports"