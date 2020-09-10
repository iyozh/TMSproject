# Generated by Django 3.1.1 on 2020-09-03 10:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("onboarding", "0009_auto_20200903_1349"),
        ("blog", "0005_auto_20200829_1125"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="onboarding.profile",
            ),
        ),
    ]
