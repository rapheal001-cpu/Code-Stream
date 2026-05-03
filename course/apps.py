from django.apps import AppConfig


class CourseConfig(AppConfig):
  name = 'course'
  def ready(self):
    from . import signal