"""
Django settings for CodeStream project.
***Räph Tëch***
"""

import os
from decouple import config
from pathlib import Path
from .utils import (
    index_view,
    login_view,
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = ['127.0.0.1','7e4e-102-223-1-130.ngrok-free.app']

#config("ALLOWED_HOSTS", cast=str).split(",")

CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.app",
]


AUTH_USER_MODEL = "accounts.User"


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Apps
    "accounts.apps.AccountsConfig",
    "core.apps.CoreConfig",
    "course.apps.CourseConfig",
    "payments.apps.PaymentsConfig",
    # Allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "widget_tweaks",
    "django_htmx",
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]


ACCOUNT_FORMS = {
    "signup": "accounts.forms.CustomSignupForm",
    "login": "accounts.forms.CustomLoginForm",
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # Allauth Account Middleware
    "allauth.account.middleware.AccountMiddleware",
    # Django Htmx Middleware
    "django_htmx.middleware.HtmxMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "CodeStream.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "CodeStream.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/


# Static
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    # Accounts Static
    os.path.join(BASE_DIR / "accounts" / "static"),
    # Core Static
    os.path.join(BASE_DIR / "core" / "static"),
    # Course Static
    os.path.join(BASE_DIR / "course" / "static"),
]


# Media
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR / "mediafiles")


# Login System
LOGIN_REDIRECT_URL = index_view
LOGOUT_REDIRECT_URL = login_view
LOGOUT_URL = login_view


# Allauth Permissions
ACCOUNT_SIGNUP_FIELDS = [
    "first_name*",
    "last_name*",
    "username*",
    "email*",
    "password1*",
    "password2*",
]
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[CodeStream]"
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_UNIQUE_USERNAME = True
ACCOUNT_RATE_LIMITS = {
    "change_password": "5/5m/user",
    "manage_email": "5/5m/user",
    "reset_password": "5/5m/ip,5/5m/key",
    "reset_password_from_key": "5/5m/ip",
    "signup": "5/5m/ip",
    "login": "5/5m/ip",
    "login_failed": "8/5m/ip,5/5m/key",
    "confirm_email": "5/5m/key",
}
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {"EMAIL_AUTHENTICATION": True, "FETCH_USERINFO": True},
    "github": {"VERIFIED_EMAIL": True},
}
ACCOUNT_ADAPTER = "accounts.adapter.CustomAdapter"


# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", cast=str)
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", cast=str)

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Stripe Secret Key
STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY", cast=str)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", cast=str)
STRIPE_WEBHOOK_SECRET_KEY = config("STRIPE_WEBHOOK_SECRET_KEY", cast=str)
