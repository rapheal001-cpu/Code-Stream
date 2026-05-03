from django.urls import path

from .views import (
  CourseView,
  CourseDetailView,
  CreateCourseView,
  CreateCourseDoneView,
  UpdateCourseView,
  CourseInfoView,
  #     CourseVideosView,
  #     CourseVideoDetailView,
)

app_name = "course"

urlpatterns = [
  # Index
  path("info/<slug:slug>/", CourseInfoView.as_view(), name="course-info"),
  path("", CourseView.as_view(), name="course-index"),
  path("<slug:slug>/", CourseDetailView.as_view(), name="course-detail"),
  path("create/course/", CreateCourseView.as_view(), name="create-course"),
  path("create/course/done/<slug:slug>/", CreateCourseDoneView.as_view(), name="create-course-done"),
  path("update/course/<slug:slug>/", UpdateCourseView.as_view(), name="update-course"),
  # Course Videos
  #     path("videos/", CourseVideosView.as_view(), name="course-videos"),
  #     path("videos/<int:pk>/", CourseVideoDetailView.as_view(), name="course-video-detail"),
]
