from src.file_utils import get_content
from src.json_utils import get_json
from src.path import EDUCATION, PORTFOLIO, THEME
from src.responses import respond_200
from src.session_utils import load_user_session
from src.stats import visits_counter
from src.theme_utils import change_mode, switch_color


def edu_handler(server, method, path):
    switcher = {
        "get": get_edu_page,
        "post": post_edu_page,
    }
    handler = switcher[method]

    handler(server, path, "/education")


def post_edu_page(server, path, endpoint):
    switcher = {"/education/night_mode": change_mode}
    handler = switcher[path]

    handler(server, path, endpoint)


def get_edu_page(server, path, redirect):
    visits_counter(path)
    theme_session = load_user_session(server, THEME)
    theme = switch_color(theme_session)
    edu_info = get_json(EDUCATION)
    file_name = PORTFOLIO / "education" / "index.html"
    content = get_content(file_name).format(**edu_info, **theme)
    respond_200(server, content, "text/html")
