import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View

from path import SESSION
from utils.session_utils import (load_user_session, parse_user_sessions,
                                 save_user_session)
from utils.stats_utils import visits_counter
from utils.utils import age_calculating, name_calculating, parse_function

year = datetime.datetime.now().year
hour = datetime.datetime.now().hour


class HelloView(View):
    def get(self, request, **kwargs):
        visits_counter(request.path)
        sessions = load_user_session(request, SESSION) or parse_function(request.path)

        name = name_calculating(sessions)
        age = age_calculating(sessions)

        born = None

        if age:
            born = year - age

        ctx = {"name": name, "year": born}

        return render(request, "hello/hello.html", ctx)

    def post(self, request):
        form = parse_user_sessions(request)
        session = load_user_session(request, SESSION)
        session.update(form)
        session_id = save_user_session(request, session, SESSION)
        response = HttpResponseRedirect("/hello")
        response.set_cookie("SESSION_ID", session_id)
        return response
