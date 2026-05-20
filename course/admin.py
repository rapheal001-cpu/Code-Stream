from django.contrib import admin
from .models import Course, CourseVideo, Enrollment, ShortVideo


@admin.register(Course)
class CustomCourse(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("name",)}


admin.site.register(CourseVideo)
admin.site.register(Enrollment)
admin.site.register(ShortVideo)
