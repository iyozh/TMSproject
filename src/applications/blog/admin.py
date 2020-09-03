from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from applications.blog.models import Post


@admin.register(Post)
class ProfileAdminModel(ModelAdmin):
    pass
