from django.db import models


class Project(models.Model):
    project_name = models.TextField(unique=True)
    started = models.DateField(null=True, blank=True)
    ended = models.DateField(null=True, blank=True)
    project_description = models.TextField(null=True, blank=True)
