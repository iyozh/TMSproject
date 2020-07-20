from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from django.views.decorators.http import require_http_methods

import datetime



from path import SESSION, HELLO_PAGE
from utils.stats_utils import visits_counter
from utils.file_utils import get_content
from utils.session_utils import load_user_session, parse_user_sessions, save_user_session
from utils.utils import parse_function, name_calculating, age_calculating


year = datetime.datetime.now().year
hour = datetime.datetime.now().hour

class HelloView(View):
    def get(self,request,**kwargs):
        visits_counter(request.path)
        sessions = load_user_session(request,SESSION) or parse_function(request.path)

        name = name_calculating(sessions)
        age = age_calculating(sessions)

        born = None

        if age:
            born = year - age

        ctx = {
            "name": name,
            "year": born
        }

        return render(request,"hello/hello.html",ctx)


    def post(self,request):
        form = parse_user_sessions(request)
        session = load_user_session(request, SESSION)
        session.update(form)
        session_id = save_user_session(request, session, SESSION)
        response = HttpResponseRedirect("/hello")
        response.set_cookie("SESSION_ID", session_id)
        return response