import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View

from path import SESSION
from utils.session_utils import (load_user_session, parse_user_sessions,
                                 save_user_session)
from utils.stats_utils import visits_counter
from utils.theme_utils import get_theme
from utils.utils import age_calculating, name_calculating, parse_function, linearize_qs

year = datetime.datetime.now().year
hour = datetime.datetime.now().hour


class HelloView(View):
    def get(self, request, **kwargs):
        visits_counter(request.path)
        sessions = load_user_session(self.request) or parse_function(request.path)

        name = name_calculating(sessions)
        age = age_calculating(sessions)

        born = None

        if age:
            born = year - age
        theme = get_theme(self.request)
        ctx = {"name": name, "year": born, "theme": theme}

        return render(request, "hello/hello.html", ctx)

    def post(self, request):
        form_content = linearize_qs(self.request.POST)
        name = name_calculating(form_content)
        age = age_calculating(form_content)
        self.request.session["name"] = name
        self.request.session["age"] = age

        # save_user_session(self.request, session, SESSION)
        response = HttpResponseRedirect("/hello")
        return response
