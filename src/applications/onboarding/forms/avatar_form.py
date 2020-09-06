from django import forms

from applications.onboarding.models import Avatar


class AvatarForm(forms.ModelForm):
    original = forms.FileField(label="Avatar")

    class Meta:
        model = Avatar
        fields = ["original"]
