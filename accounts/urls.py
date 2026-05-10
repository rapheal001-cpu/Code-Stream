from django.urls import (
    path,
    re_path,
    include,
)

from .views import (
    signup_view,
    login_view,
    logout_view,
    email_verification_sent_view,
    confirm_email_view,
    password_reset_view,
    password_reset_done_view,
    password_reset_from_key_view,
    password_reset_from_key_done_view,
    login_cancelled_view,
    login_error_view,
    social_connections_view,
    profile_view,
    update_profile_view,
    description_view,
    settings_view,
    profile_views_list,
    email_view,
    password_change_view,
    password_change_done_view,
    password_set_view,
    password_set_done_view,
    notification_view,
    notification_detail_view,
    find_friend_view,
    instructor_wallet_view,
    instructor_course_view,
    follow_view,
    followers_and_following_view,
    followers_view,
    following_view,

)

urlpatterns = [
    path('following/<int:pk>/', following_view, name="following-view"),
    path('followers/<int:pk>/', followers_view, name="followers-view"),
    path(
        "followers-and-following/<int:pk>/",
        followers_and_following_view,
        name="followers-and-following-view",
    ),
    path("follow/<int:pk>/", follow_view, name="follow-view"),
    path("my-course/", instructor_course_view, name="instructor-courses"),
    path("wallet/<int:pk>/", instructor_wallet_view, name="wallet"),
    path("find-friends/", find_friend_view, name="find-friends"),
    path(
        "notification-detail/<int:pk>/", notification_detail_view,
        name="notification-detail",
    ),
    path("notifications/", notification_view, name="notification"),
    path("profile-views/", profile_views_list, name="profile-views"),
    path("my-description/", description_view, name="description"),
    path("settings/", settings_view, name="settings"),
    path(
        "3rdparty/", social_connections_view, name="socialaccount_connections"
    ),
    path(
        "3rdparty/login/error/",
        login_error_view,
        name="socialaccount_login_error",
    ),
    path(
        "3rdparty/login/cancelled/",
        login_cancelled_view,
        name="socialaccount_login_cancelled",
    ),
    path(
        "password/change/done/",
        password_change_done_view,
        name="password_change_done",
    ),
    path(
        "password/change/",
        password_change_view,
        name="account_change_password",
    ),
    path(
        "password/set/done/",
        password_set_done_view,
        name="password_set_done",
    ),
    path("password/set/", password_set_view, name="account_set_password"),
    path("email/", email_view, name="account_email"),
    path("update-profile/", update_profile_view, name="update-profile"),
    path("profile/<int:pk>/", profile_view, name="profile"),
    path(
        "password/reset/key/done/",
        password_reset_from_key_done_view,
        name="account_reset_password_from_key_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        password_reset_from_key_view,
        name="account_reset_password_from_key",
    ),
    path(
        "password/reset/done/", password_reset_done_view,
        name="account_reset_password_done",
    ),
    path(
        "password/reset/", password_reset_view,
        name="account_reset_password",
    ),
    path("login/", login_view, name="account_login"),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        confirm_email_view,
        name="account_confirm_email",
    ),
    path(
        "confirm-email/",
        email_verification_sent_view,
        name="account_email_verification_sent",
    ),
    path("logout/", logout_view, name="account_logout"),
    path("signup/", signup_view, name="account_signup"),
    # Allauth Urls
    path("", include("allauth.urls")),
]
