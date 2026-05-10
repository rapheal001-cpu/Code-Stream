from django.urls import path
from .views import (index_view, about_view,)

app_name = "core"

urlpatterns = [
    path("", index_view, name="index-view"),
    path("about/", about_view, name="about-view"),
]
