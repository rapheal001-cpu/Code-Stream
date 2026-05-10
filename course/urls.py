from django.urls import path

from .views import (
    course_view,
    course_detail_view,
    create_course_view,
    create_course_done_view,
    update_course_view,
    course_info_view,
)

app_name = "course"

urlpatterns = [
    # Index
    path("info/<int:pk>/", course_info_view, name="course-info"),
    path("", course_view, name="course-index"),
    path("<int:pk>/", course_detail_view, name="course-detail"),
    path("create-course/", create_course_view, name="create-course"),
    path( "create-course-done/<int:pk>/", create_course_done_view, name="create-course-done"),
    path("update-course/<int:pk>/", update_course_view, name="update-course"),
]
