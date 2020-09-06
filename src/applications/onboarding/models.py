from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from storages.backends.s3boto3 import S3Boto3Storage

User = get_user_model()

def upload_to(instance:"Avatar",filename):
    return f"{settings.AWS_S3_AVATARS_LOCATION}/avatar_{instance.pk}_{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    display_name = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "profile"

    def __str__(self):
        return f"{self.display_name}"


class Avatar(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,primary_key=True)
    original = models.FileField(storage=S3Boto3Storage(),upload_to=upload_to,null=True,blank=True)

    class Meta:
        verbose_name_plural = "avatar"

    def __str__(self):
        return f"Avatar(user = {self.profile})"