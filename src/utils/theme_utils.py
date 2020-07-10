

from src.path import THEME
from src.responses import respond_302
from src.utils.session_utils import load_user_session, save_user_session



def change_mode(server, path, redirect):
    theme_session = load_user_session(server, THEME)
    theme = switch_color(theme_session)
    theme["background_color"], theme["text_color"] = (
        theme["text_color"],
        theme["background_color"],
    )

    session_id = save_user_session(server, theme, THEME)
    respond_302(server, redirect, session_id)


def switch_color(theme):
    if not theme:
        theme["background_color"] = "white"
        theme["text_color"] = "black"

    return theme
