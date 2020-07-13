from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from path import EDUCATION, PORTFOLIO, THEME

from pages.stats import visits_counter
from utils.file_utils import get_content
from utils.json_utils import get_json
from utils.session_utils import load_user_session
from utils.theme_utils import switch_color, change_mode

@require_http_methods(['GET', 'POST'])
def edu_handler(request):
    switcher = {
        "GET": get_edu_page,
        "POST": post_edu_page,
    }
    handler = switcher[request.method]

    return handler(request,"/education")


def post_edu_page(request,redirect):
    switcher = {"/education/night_mode": change_mode}
    handler = switcher[request.path]

    return handler(request,redirect)


def get_edu_page(request, redirect):
    visits_counter(request.path)
    theme_session = load_user_session(request, THEME)
    theme = switch_color(theme_session)
    edu_info = get_json(EDUCATION)
    file_name = PORTFOLIO / "education" / "index.html"
    content = get_content(file_name).format(**edu_info, **theme)
    return HttpResponse(content)