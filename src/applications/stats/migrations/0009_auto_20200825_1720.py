# Generated by Django 3.1 on 2020-08-25 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0008_stats_size"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stats",
            name="size",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
