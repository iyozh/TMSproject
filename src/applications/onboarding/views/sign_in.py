from django.contrib.auth.views import LoginView

from utils.stats_utils import count_stats


@count_stats
class SignInView(LoginView):
    template_name = "onboarding/sign_in.html"