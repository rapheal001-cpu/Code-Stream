from django.urls import path

from .views import IndexView, AboutView

app_name = "core"

urlpatterns = [
  path("", IndexView.as_view(), name="index-view"),
  path("about/", AboutView.as_view(), name="about-view"),
]
