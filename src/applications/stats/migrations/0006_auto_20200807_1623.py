# Generated by Django 3.0.8 on 2020-08-07 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0005_auto_20200807_1618"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stats",
            name="user",
            field=models.TextField(blank=True, null=True),
        ),
    ]
