"""
URL configuration for CodeStream project.
"""

from django.contrib import admin
from django.urls import (
    path,
    include,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Fake Admin Login
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # Admin
    path("code-stream-admin/", admin.site.urls),
    # Accounts
    path("accounts/", include("accounts.urls")),
    # Course
    path("course/", include("course.urls", namespace="course")),
    # Core
    path("", include("core.urls", namespace="core")),
    # Payments
    path("payment/", include("payments.urls", namespace="payment")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
