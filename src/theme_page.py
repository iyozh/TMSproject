from src.file_utils import get_content
from src.path import THEME, THEME_INDEX
from src.responses import respond_200
from src.session_utils import load_user_session
from src.stats import visits_counter
from src.theme_utils import change_mode, switch_color


def theme_handler(server, method, path):
    switcher = {"get": get_theme_page, "post": post_theme_page}
    handler = switcher[method]
    handler(server, path, "/theme")


def post_theme_page(server, path, endpoint):
    switcher = {"/theme/night_mode": change_mode}
    handler = switcher[path]

    handler(server, path, endpoint)


def get_theme_page(server, path, redirect):
    visits_counter(path)
    theme_session = load_user_session(server, THEME)
    theme = switch_color(theme_session)
    theme_page = get_content(THEME_INDEX).format(**theme)
    respond_200(server, theme_page, "text/html")
