from django.urls import path

from .views import (
    CourseView,
    CourseDetailView,
    CreateCourseView,
    CreateCourseDoneView,
    UpdateCourseView,
    CourseInfoView,
)

app_name = "course"

urlpatterns = [
    # Index
    path("info/<int:pk>/", CourseInfoView.as_view(), name="course-info"),
    path("", CourseView.as_view(), name="course-index"),
    path("<int:pk>/", CourseDetailView.as_view(), name="course-detail"),
    path("create-course/", CreateCourseView.as_view(), name="create-course"),
    path(
        "create-course-done/<int:pk>/",
        CreateCourseDoneView.as_view(),
        name="create-course-done",
    ),
    path("update-course/<int:pk>/", UpdateCourseView.as_view(), name="update-course"),
]
