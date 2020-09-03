from django import forms
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin

from applications.onboarding.models import Profile
from path import EDUCATION
from utils.json_utils import get_json
from utils.stats_utils import count_stats

User = get_user_model()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"


class CurrentUserMixin:
    def get_object(self, queryset=None):

        if self.request.user.is_anonymous:
            return None

        if not queryset:
            queryset = self.model.objects.all()
        queryset = queryset.filter(user=self.request.user)
        return queryset.first()


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


@count_stats
class SignInView(LoginView):
    template_name = "onboarding/sign_in.html"


@count_stats
class SignOutView(LogoutView):
    template_name = "onboarding/signed_out.html"


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


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

        return super().form_valid(form)


@count_stats
class ProfileUpdateView(CurrentUserMixin, UpdateView):
    http_method_names = ["post"]
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy("onboarding:profile")
