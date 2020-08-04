from django.db import models

# Create your models here.


class Stats(models.Model):
    url = models.TextField()
    date = models.DateField()