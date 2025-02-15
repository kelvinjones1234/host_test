from django.db import models

class ApiSettings(models.Model):
  api_name = models.CharField(max_length=200, null=True, blank=True)
  api_key = models.CharField(max_length=1000, null=True, blank=True)
  active = models.BooleanField(default=False)

  def __str__(self):
    return self.api_name
