from django.urls import path

from .views import (
    course_view,
    course_detail_view,
    create_course_view,
    create_course_done_view,
    update_course_view,
    course_info_view,
)

urlpatterns = [
    path("info/<int:pk>/", course_info_view, name="course-info-view"),
    path("", course_view, name="course-index-view"),
    path("create-course/", create_course_view, name="create-course-view"),
    path("create-course-done/<int:pk>/", create_course_done_view, name="create-course-done-view"),
    path("update-course/<int:pk>/", update_course_view, name="update-course-view"),
    path("detail/<slug:slug>/", course_detail_view, name="course-detail-view"),
]