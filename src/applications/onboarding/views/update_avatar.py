from django.urls import reverse_lazy
from django.views.generic import UpdateView

from applications.onboarding.forms import AvatarForm
from applications.onboarding.mixins import CurrentUserMixin
from applications.onboarding.models import Avatar


class AvatarUpdate(CurrentUserMixin, UpdateView):
    model = Avatar
    form_class = AvatarForm
    http_method_names = ["post"]
    success_url = reverse_lazy("onboarding:profile")

    def get_object(self, queryset=None):
        return self.get_current_avatar()
