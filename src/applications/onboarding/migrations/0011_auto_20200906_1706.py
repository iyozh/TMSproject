# Generated by Django 3.1.1 on 2020-09-06 14:06

import applications.onboarding.models
from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0010_auto_20200906_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='original',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(), upload_to=applications.onboarding.models.upload_to),
        ),
    ]
