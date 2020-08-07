from django.db import models

# Create your models here.


class Stats(models.Model):
    url = models.URLField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    method = models.TextField(null=True, blank=True)
    user = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["pk"]
