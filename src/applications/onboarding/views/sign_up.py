from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import FormView

from applications.onboarding.forms import SignUpForm
from applications.onboarding.models import Profile, Avatar
from utils.stats_utils import count_stats


@count_stats
class SignUpView(FormView):
    template_name = "onboarding/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy("onboarding:profile")

    def form_valid(self, form):
        form.save()

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]

        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        profile = Profile(user=user, display_name=username)
        profile.save()
        avatar = Avatar(original=None,profile=profile)
        avatar.save()

        return super().form_valid(form)