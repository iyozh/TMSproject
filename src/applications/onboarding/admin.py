from django import forms
from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from applications.onboarding.models import Profile


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {"display_name": forms.TextInput(attrs={"style": "width:200px"})}


@admin.register(Profile)
class ProfileAdminModel(ModelAdmin):
    pass
