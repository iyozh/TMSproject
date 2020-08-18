from django.db import models
from django.urls import reverse_lazy


class Project(models.Model):
    name = models.TextField(unique=True)
    started = models.DateField(null=True, blank=True)
    ended = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    visible = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse_lazy("test_projects:c_project", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.__class__.__name__}({self.name},id = {self.pk})"

    class Meta:
        verbose_name_plural = "project"
