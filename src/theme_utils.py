from src.session_utils import load_user_session,save_user_session
from src.responses import respond_302
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.resolve()
THEME = PROJECT_DIR / "data" / "theme.json"


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