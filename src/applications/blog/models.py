from django.db import models

# Create your models here.
from django.urls import reverse_lazy


class Post(models.Model):
    user = models.TextField(unique=True)
    date = models.DateField(null=True, blank=True)
    content = models.TextField(null=True, blank=True, max_length=140)

    def __str__(self):
        return f"{self.__class__.__name__}({self.user},id = {self.pk})"

    def get_absolute_url(self):
        return reverse_lazy("blog:post", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "post"
