from django.urls import path

from applications.onboarding.apps import OnboardingConfig
from applications.onboarding.views import (
    MyProfileView,
    ProfileUpdateView,
    SignInView,
    SignOutView,
    SignUpView,
)

app_name = OnboardingConfig.label

urlpatterns = [
    path("", MyProfileView.as_view(), name="profile"),
    path("sign-in/", SignInView.as_view(), name="sign-in"),
    path("sign-out/", SignOutView.as_view(), name="sign-out"),
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("update/", ProfileUpdateView.as_view(), name="update"),
]
