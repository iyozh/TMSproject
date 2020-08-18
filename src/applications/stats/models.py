import datetime

from django.db import models

# Create your models here.


class Stats(models.Model):
    url = models.URLField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    method = models.TextField(null=True, blank=True)
    code = models.IntegerField(null=True, blank=True)
    user = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    # def generate_dashboard(cls):
    #     errors = {}
    #     today = datetime.datetime.now()
    #     time = Q(date_gte=today - timedelta)
    #     m5 = Stats.objects.filter()
