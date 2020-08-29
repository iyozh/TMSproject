# Generated by Django 3.1 on 2020-08-26 18:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200826_1923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.utcnow, editable=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.TextField(default=None, editable=False),
        ),
    ]
