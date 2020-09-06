from django.urls import reverse_lazy
from django.views.generic import UpdateView

from applications.onboarding.forms import ProfileForm
from applications.onboarding.models import Profile
from applications.onboarding.mixins import CurrentUserMixin
from utils.stats_utils import count_stats


@count_stats
class ProfileUpdateView(CurrentUserMixin, UpdateView):
    http_method_names = ["post"]
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy("onboarding:profile")

