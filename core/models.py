from django.db import models
# Create your models here.

######################################
# Report
class Report(models.Model):
  user_identifier = models.CharField(max_length=50)
  topic = models.CharField(max_length=500)
  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    res = f"{self.user_identifier} Report"
    return res
    
  class Meta:
    ordering = ["-created_at"]
    verbose_name_plural = "Report"