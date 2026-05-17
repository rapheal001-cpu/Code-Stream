from django.db import models
# Create your models here.


######################################
# Report
class Report(models.Model):
    user_identifier = models.CharField(max_length=50, verbose_name="User Identifier")
    topic = models.CharField(max_length=500, verbose_name="Topic")
    body = models.TextField(verbose_name="Body")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return f"{self.user_identifier} Report"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Report"
        verbose_name_plural = "Reports"