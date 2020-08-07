from django.db import models


class Project(models.Model):
    project_name = models.TextField(unique=True)
    started = models.DateField(null=True, blank=True)
    ended = models.DateField(null=True, blank=True)
    project_description = models.TextField(null=True, blank=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.__class__.__name__}({self.project_name},id = {self.pk})"

    class Meta:
        verbose_name_plural = "project"
