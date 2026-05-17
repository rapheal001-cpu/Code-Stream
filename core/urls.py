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
    find_friend_view,
    instructor_wallet_view,
    instructor_course_view,
    follow_toggle_view,
)

app_name = "core"

urlpatterns = [
    path("", index_view, name="index-view"),
    path("about/", about_view, name="about-view"),
    path("follow/<int:pk>/", follow_toggle_view, name="follow-toggle-view"),
    path("my-course/", instructor_course_view, name="instructor-courses"),
    path("wallet/<int:pk>/", instructor_wallet_view, name="wallet"),
    path("find-friends/", find_friend_view, name="find-friends"),
    path("notification-detail/<int:pk>/", notification_detail_view, name="notification-detail", ),
    path("notifications/", notification_view, name="notification"),
    path("profile-views/", profile_list_views, name="profile-views"),
    path("my-description/", description_view, name="description"),
    path("settings/", settings_view, name="settings"),
    path("update-profile/", update_profile_view, name="update-profile"),
    path("profile/<int:pk>/", profile_view, name="profile"),
]
