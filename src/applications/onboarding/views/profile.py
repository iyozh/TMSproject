from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from applications.onboarding.forms import ProfileForm, AvatarForm
from applications.onboarding.mixins import CurrentUserMixin
from applications.onboarding.models import Profile
from utils.stats_utils import count_stats


@count_stats
class MyProfileView(CurrentUserMixin, FormMixin, LoginRequiredMixin, DetailView):
    template_name = "onboarding/index.html"
    model = Profile
    form_class = ProfileForm

    def get_initial(self):
        return {
            Profile.display_name.field.name: self.object.display_name,
            Profile.birth_date.field.name: self.object.birth_date,
        }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["avatar_form"] = AvatarForm()
        return ctx