from django.http import HttpResponseRedirect

from path import THEME

from utils.session_utils import load_user_session, save_user_session



def change_mode(request,redirect):
    theme_session = load_user_session(request, THEME)
    theme = switch_color(theme_session)
    theme["background_color"], theme["text_color"] = (
        theme["text_color"],
        theme["background_color"],
    )

    session_id = save_user_session(request, theme, THEME)
    response = HttpResponseRedirect(redirect)
    response.set_cookie("SESSION_ID", session_id)
    return response


def switch_color(theme):
    if not theme:
        theme["background_color"] = "white"
        theme["text_color"] = "black"

    return theme