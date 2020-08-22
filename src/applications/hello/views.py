import datetime
from typing import NamedTuple

from django import forms
from django.urls import reverse_lazy
from django.views.generic import FormView

from utils.session_utils import load_user_session
from utils.stats_utils import count_stats
from utils.utils import age_calculating, name_calculating, parse_function

year = datetime.datetime.now().year
hour = datetime.datetime.now().hour


class HelloForm(forms.Form):
    name = forms.CharField(max_length=200)
    age = forms.IntegerField(required=False, min_value=0)


@count_stats
class HelloView(FormView):
    template_name = "hello/hello.html"
    success_url = reverse_lazy("hello:hello")
    form_class = HelloForm

    def get_initial(self):
        user = self.build_name_age()
        ready_user = user._asdict()
        return ready_user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        name, age = self.build_name_age()

        born = None

        if age is not None:
            born = year - age

        ctx.update({"name": name, "year": born})
        return ctx

    def form_valid(self, form):
        self.request.session["name"] = form.cleaned_data["name"]
        self.request.session["age"] = form.cleaned_data["age"]
        return super().form_valid(form)

    def build_name_age(self):
        sessions = load_user_session(self.request) or parse_function(self.request)

        name = name_calculating(sessions)
        age = age_calculating(sessions)

        return UserData(name, age)


class UserData(NamedTuple):
    name: str
    age: str
