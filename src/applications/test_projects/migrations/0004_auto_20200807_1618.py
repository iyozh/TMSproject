# Generated by Django 3.0.8 on 2020-08-07 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("test_projects", "0003_project_visible"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="project", options={"verbose_name_plural": "project"},
        ),
    ]
