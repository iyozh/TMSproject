import datetime

from src.file_utils import get_content
from src.path import PROJECT_DIR, SESSION
from src.responses import respond_200, respond_302
from src.session_utils import (load_user_session, parse_user_sessions,
                               save_user_session)
from src.stats import visits_counter
from src.utils import age_calculating, name_calculating, parse_function

year = datetime.datetime.now().year
hour = datetime.datetime.now().hour


def handler_hello(server, method: str, path):
    visits_counter(path)
    switcher = {"get": hello_GETresponse, "post": hello_POSTresponse}
    handler = switcher[method]
    handler(server, path)


def hello_GETresponse(server, path):
    sessions = load_user_session(server, SESSION) or parse_function(server, path)
    name = name_calculating(sessions)
    age = age_calculating(sessions)

    born = None

    if age:
        born = year - age

    html_content = PROJECT_DIR / "hello" / "hello.html"
    hello_page = get_content(html_content).format(name=name, year=born)
    respond_200(server, hello_page, "text/html")


def hello_POSTresponse(server, path):
    form = parse_user_sessions(server)
    session = load_user_session(server, SESSION)
    session.update(form)
    session_id = save_user_session(server, session, SESSION)
    respond_302(server, "/hello", session_id)
