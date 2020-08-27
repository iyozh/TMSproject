from datetime import datetime

from django.db import models

# Create your models here.
from django.urls import reverse_lazy


class Post(models.Model):
    user = models.TextField(default="User",null=True,blank=True)
    date = models.DateTimeField(default=datetime.utcnow,editable=False)
    content = models.TextField()
    def __str__(self):
        return f"{self.__class__.__name__}({self.user},id = {self.pk})"

    def get_absolute_url(self):
        return reverse_lazy("blog:post",kwargs={"pk":self.pk})

    class Meta:
        verbose_name_plural = "post"
        ordering = ["-date"]
