from datetime import datetime

from django.db import models

# Create your models here.
from django.urls import reverse_lazy

from applications.onboarding.models import User


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField(default=datetime.utcnow, editable=False)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.__class__.__name__}({self.user},id = {self.pk})"

    def get_absolute_url(self):
        return reverse_lazy("blog:post", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "post"
        ordering = ["-date"]
