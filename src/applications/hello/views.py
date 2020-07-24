import datetime

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic.base import View

from utils.session_utils import (load_user_session)
from utils.stats_utils import visits_counter
from utils.theme_utils import get_theme, change_mode
from utils.utils import age_calculating, name_calculating, parse_function, linearize_qs

year = datetime.datetime.now().year
hour = datetime.datetime.now().hour


class HelloForm(forms.Form):
    name = forms.CharField(max_length=200)
    age = forms.IntegerField(required=False, min_value=0)


class HelloView(FormView):
    template_name = "hello/hello.html"
    success_url = "/hello/"
    form_class = HelloForm

    def dispatch(self, request, *args, **kwargs):
        visits_counter(self.request.path)
        return super().dispatch(request)


    def get_initial(self):
        name, age = self.build_name_age()
        return {
            "name": name or "",
            "age": age or None
        }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        name, age = self.build_name_age()

        born = None

        if age is not None:
            born = year - age
        theme = get_theme(self.request)
        ctx.update({"name": name, "year": born, "theme": theme})
        return ctx

    def form_valid(self, form):
        self.request.session["name"] = form.cleaned_data["name"]
        self.request.session["age"] = form.cleaned_data["age"]
        return super().form_valid(form)

    def build_name_age(self):
        sessions = load_user_session(self.request) or parse_function(self.request)

        name = name_calculating(sessions)
        age = age_calculating(sessions)

        return name, age

class NightModeView(View):

    def post(self,request):
        return change_mode(self.request, "/test_projects")