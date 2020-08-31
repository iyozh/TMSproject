from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    display_name = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True,upload_to="avatars/")

    class Meta:
        verbose_name_plural = "profile"

    def __str__(self):
        return f"{self.display_name}"
