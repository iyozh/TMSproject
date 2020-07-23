from django.http import HttpResponseRedirect


def change_mode(request, redirect):
    switch_color(request)
    return HttpResponseRedirect(redirect)


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
