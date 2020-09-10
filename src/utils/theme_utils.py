from django.views.generic import RedirectView


def change_mode(request):
    switch_color(request)


def get_theme(request):
    default_theme = {"background_color": "white", "text_color": "black"}
    request.session.set_expiry(0)
    return request.session.get("theme", default_theme)


def switch_color(request):
    current_theme = get_theme(request)
    current_theme["background_color"], current_theme["text_color"] = (
        current_theme["text_color"],
        current_theme["background_color"],
    )
    request.session["theme"] = current_theme


def theme_ctx_processor(request):
    theme = get_theme(request)
    return {"theme": theme, "object": object}


class NightModeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        change_mode(self.request)
        url = self.request.headers["Referer"]
        return url
