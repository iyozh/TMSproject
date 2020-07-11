import datetime

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from utils.file_utils import get_content
from path import PROJECT_DIR, SESSION
from utils.session_utils import (load_user_session, parse_user_sessions,
                                     save_user_session)
from utils.utils import age_calculating, name_calculating, parse_function

year = datetime.datetime.now().year
hour = datetime.datetime.now().hour


@require_http_methods(['GET', 'POST'])
def handler_hello(request):
    switcher = {"GET": hello_GETresponse, "POST": hello_POSTresponse}
    handler = switcher[request.method]
    return handler(request)


def hello_GETresponse(request):
    sessions = load_user_session(request,SESSION) or parse_function(request.path)
    name = name_calculating(sessions)
    age = age_calculating(sessions)

    born = None

    if age:
        born = year - age

    html_content = PROJECT_DIR / "hello" / "hello.html"
    hello_page = get_content(html_content).format(name=name, year=born)
    return HttpResponse(hello_page,"text/html")


def hello_POSTresponse(request):
    form = parse_user_sessions(request)
    session = load_user_session(request, SESSION)
    session.update(form)
    session_id = save_user_session(request, session, SESSION)
    response = HttpResponse()
    response["Location"] = "/hello"
    response["Cookie"] = session_id
    return response
