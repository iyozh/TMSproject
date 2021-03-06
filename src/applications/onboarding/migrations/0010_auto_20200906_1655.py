# Generated by Django 3.1.1 on 2020-09-06 13:55

import storages.backends.s3boto3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("onboarding", "0009_auto_20200903_1349"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avatar",
            name="original",
            field=models.FileField(
                storage=storages.backends.s3boto3.S3Boto3Storage(),
                upload_to="avatars-dev",
            ),
        ),
    ]
