from django.contrib.auth import get_user_model
from django.views.generic import DetailView

from applications.onboarding.models import Profile

User = get_user_model()


class ProfileView(DetailView):
    template_name = "onboarding/other_profile.html"
    model = Profile

    def get_object(self, queryset=None):
        display_name = self.kwargs["name"]
        obj = Profile.objects.filter(display_name=display_name).first()
        return obj
