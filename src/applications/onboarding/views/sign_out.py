from django.contrib.auth.views import LogoutView

from utils.stats_utils import count_stats


@count_stats
class SignOutView(LogoutView):
    template_name = "onboarding/signed_out.html"
