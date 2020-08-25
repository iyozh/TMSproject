from django import forms
from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from applications.test_projects.models import Project



class ProjectAdminForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = "__all__"
        widgets = {"name":forms.TextInput(attrs={"style":"width:200px"})}


class ProjectAdminModel(ModelAdmin):
    form = ProjectAdminForm