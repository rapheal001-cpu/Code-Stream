from django.urls import path
from .views import (
    index_view,
    about_view,
    profile_view,
    update_profile_view,
    description_view,
    settings_view,
    profile_list_views,
    notification_view,
    notification_detail_view,
    discover_developer_view,
    instructor_wallet_view,
    instructor_course_view,
)

urlpatterns = [
    path("", index_view, name="index-view"),
    path("about/", about_view, name="about-view"),
    path("my-course/", instructor_course_view, name="instructor-courses-view"),
    path("wallet/<int:pk>/", instructor_wallet_view, name="wallet-view"),
    path("discover-developers/", discover_developer_view, name="discover-developers-view"),
    path("notification-detail/<int:pk>/", notification_detail_view, name="notification-detail-view", ),
    path("notifications/", notification_view, name="notification-view"),
    path("profile-views/", profile_list_views, name="profile-list-views"),
    path("my-description/", description_view, name="description-view"),
    path("settings/", settings_view, name="settings-view"),
    path("update-profile/", update_profile_view, name="update-profile-view"),
    path("profile/<int:pk>/", profile_view, name="profile-view"),
]
