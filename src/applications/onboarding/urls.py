from django.urls import path

from applications.onboarding.apps import OnboardingConfig
from applications.onboarding.views import (
    MyProfileView,
    ProfileUpdateView,
    ProfileView,
    SignInView,
    SignOutView,
    SignUpView,
)
from applications.onboarding.views.update_avatar import AvatarUpdate

app_name = OnboardingConfig.label

urlpatterns = [
    path("", MyProfileView.as_view(), name="profile"),
    path("sign-in/", SignInView.as_view(), name="sign-in"),
    path("sign-out/", SignOutView.as_view(), name="sign-out"),
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("update/", ProfileUpdateView.as_view(), name="update_profile"),
    path("update_avatar/", AvatarUpdate.as_view(), name="update_avatar"),
    path("<str:name>/", ProfileView.as_view(), name="other-profile"),
]
