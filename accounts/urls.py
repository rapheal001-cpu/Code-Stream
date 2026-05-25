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
    email_view,
    password_change_view,
    password_change_done_view,
    password_set_view,
    password_set_done_view,
)

urlpatterns = [
    # Allauth Social Account Override
    path("3rdparty/", social_connections_view, name="socialaccount_connections"),
    path("3rdparty/login/error/",login_error_view,name="socialaccount_login_error",),
    path("3rdparty/login/cancelled/", login_cancelled_view, name="socialaccount_login_cancelled",),
    # Allauth Account Override
    path("password/change/done/",password_change_done_view,name="password_change_done",),
    path("password/change/",password_change_view,name="account_change_password",),
    path("password/set/done/",password_set_done_view,name="password_set_done",),
    path("password/set/", password_set_view, name="account_set_password"),
    path("email/", email_view, name="account_email"),
    path("password/reset/key/done/",password_reset_from_key_done_view,name="account_reset_password_from_key_done",),
    path("password/reset/done/", password_reset_done_view, name="account_reset_password_done", ),
    path("password/reset/", password_reset_view, name="account_reset_password", ),
    path("login/", login_view, name="account_login"),
    path("confirm-email/", email_verification_sent_view, name="account_email_verification_sent", ),
    path("logout/", logout_view, name="account_logout"),
    path("signup/", signup_view, name="account_signup"),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$",confirm_email_view,name="account_confirm_email",),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",password_reset_from_key_view,name="account_reset_password_from_key",),
    # Allauth URLS
    path("", include("allauth.urls")),
]
