from django.urls import path

from .views import (
    course_index_view,
    course_action_delete_and_like_view,
    course_detail_view,
    course_video_action_delete_view,
    create_course_view,
    create_course_done_view,
    update_course_view,
    update_course_done_view,
    course_info_view,
    create_course_video_view,
    update_course_video_view,
)

urlpatterns = [
    path("", course_index_view, name="course-index-view"),
    path('action/', course_action_delete_and_like_view, name='course-action-view'),
    path('video-delete/', course_video_action_delete_view, name="course-video-delete-view"),
    path("create/", create_course_view, name="create-course-view"),
    path("create-done/<int:pk>/", create_course_done_view, name="create-course-done-view"),
    path("update/<int:pk>/", update_course_view, name="update-course-view"),
    path("update-done/<int:pk>/", update_course_done_view, name="update-course-done-view"),
    path("info/<int:pk>/", course_info_view, name="course-info-view"),
    path('create-video/<int:course_id>/', create_course_video_view, name="create-course-video-view"),
    path('update-video/<int:pk>/', update_course_video_view, name="update-course-video-view"),
    path("detail/<int:pk>/", course_detail_view, name="course-detail-view"),
]